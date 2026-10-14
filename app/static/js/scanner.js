let scannerRunning = false;
let detectionHandler = null;

function startScanner(onCodeDetected, targetSelector = '#interactive') {
    if (!window.Quagga) {
        alert('El módulo del escáner no está disponible. Puedes ingresar el código manualmente.');
        return;
    }

    const target = document.querySelector(targetSelector);
    if (!target) {
        console.error(`No existe el contenedor del escáner: ${targetSelector}`);
        return;
    }

    stopScanner();

    if (!navigator.mediaDevices?.getUserMedia) {
        alert('Tu navegador no permite acceder a la cámara desde esta página.');
        return;
    }

    Quagga.init({
        inputStream: {
            name: 'Live',
            type: 'LiveStream',
            target,
            constraints: {
                facingMode: 'environment'
            }
        },
        decoder: {
            readers: [
                'ean_reader',
                'ean_8_reader',
                'code_128_reader',
                'code_39_reader',
                'upc_reader',
                'upc_e_reader'
            ]
        }
    }, function (error) {
        if (error) {
            console.error('No se pudo iniciar el escáner:', error);
            alert('No fue posible iniciar la cámara. Revisa los permisos del navegador o usa el ingreso manual.');
            return;
        }

        scannerRunning = true;
        Quagga.start();
    });

    detectionHandler = function (result) {
        const code = result?.codeResult?.code;
        if (!code) return;

        stopScanner();
        onCodeDetected(code);
    };

    Quagga.onDetected(detectionHandler);
}

function stopScanner() {
    if (!window.Quagga) return;

    if (detectionHandler) {
        Quagga.offDetected(detectionHandler);
        detectionHandler = null;
    }

    if (scannerRunning) {
        Quagga.stop();
        scannerRunning = false;
    }
}
