let copyConfBtns = document.getElementsByClassName('conf-copy')
let generateQRBtns = document.getElementsByClassName('conf-qr')
let downloadConfBtns = document.getElementsByClassName('conf-download')


window.addEventListener("load", function () {
    for (let i = 0; i < downloadConfBtns.length; i++) {
        let configParagraphs = downloadConfBtns[i].parentElement.parentElement.getElementsByTagName('p')
        wgConfig = getWgConfig(configParagraphs)
        downloadConfBtns[i].href = 'data:text/plain;charset=utf-8,' + encodeURIComponent(wgConfig)
        downloadConfBtns[i].download = 'wg.conf'
    }
});


for (let i = 0; i < copyConfBtns.length; i++) {
    copyConfBtns[i].addEventListener('click', function () {
        let configParagraphs = this.parentElement.parentElement.getElementsByTagName('p')
        wgConfig = getWgConfig(configParagraphs)
        navigator.clipboard.writeText(wgConfig)
    })
}


for (let i = 0; i < generateQRBtns.length; i++) {
    generateQRBtns[i].addEventListener('click', function () {
        let configParagraphs = this.parentElement.parentElement.getElementsByTagName('p')
        let qrCanvas = this.parentElement.parentElement.getElementsByTagName('canvas')[0]
        let qrDownload = qrCanvas.parentElement
        let qrBlock = qrDownload.parentElement

        qrBlock.classList.remove('d-none')

        wgConfig = getWgConfig(configParagraphs)
        makeQR(wgConfig, qrCanvas, qrDownload)
    })
}


function getWgConfig(configParagraphs) {
    let configParts = []

    for (let i = 0; i < configParagraphs.length; i++) {
        let configPart = configParagraphs[i].textContent
        let normalizedConf = normalizeConfigRaws(configPart)
        configParts.push(normalizedConf)
    }

    return configParts.join('\r\n\r\n')
}


function normalizeConfigRaws(confRaws) {
    confRaws = confRaws.split(/\r?\n/)
    confRaws = confRaws.map((raw) => raw.trim())
    confRaws = confRaws.filter(n => n).join('\r\n')
    return confRaws
}


const makeQR = (qrData, qrContainer, qrDownload) => {
    new QRious({
        element: qrContainer,
        value: qrData,
        size: 250,
        padding: 10,
    });
    downloadQR(qrDownload, qrContainer)
}

function downloadQR(link, qrElement) {
    link.download = 'wg_conf.png';
    link.href = qrElement.toDataURL()
}
