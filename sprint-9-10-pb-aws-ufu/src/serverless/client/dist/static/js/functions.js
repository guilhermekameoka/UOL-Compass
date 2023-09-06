    document.addEventListener("DOMContentLoaded", function () {
    const comecePorAqui = document.getElementById('B1');
    const artigos = document.getElementById('artigos');
    
    const comecePorAquiMobile = document.getElementById('btn-1-mobile');
    const artigosMobile = document.getElementById('btn-2-mobile');
    
    
    const closeButton = document.getElementById('close');
    const closeButtonArtigos = document.getElementById('close-artigos');

    const modal = document.getElementById('modal');
    const modalartigos = document.getElementById('modal-artigos');

    
    const section1 = document.getElementById('s1');

    comecePorAqui.addEventListener("click", function () {
        toggleModal(modal);
    });
  
    comecePorAquiMobile.addEventListener("click", function () {
        toggleModal(modal);
    });

    artigos.addEventListener("click", function () {
        toggleModal(modalartigos);
    });
  
    artigosMobile.addEventListener("click", function () {
        toggleModal(modalartigos);
    });

    closeButton.addEventListener("click", function () {
        if (modal.style.display == 'block') {
            toggleModal(modal);
        }
    });

    closeButtonArtigos.addEventListener("click", function () {
        if (modalartigos.style.display == 'block') {
            toggleModal(modalartigos);
        }
    });

    function toggleModal(modalElement) {
        if (modalElement.style.display == 'none' || modalElement.style.display === '') {
            modalElement.style.display = 'block';
            blurEvent(section1);
        } else {
            modalElement.style.display = 'none';
            uncheckBlur(section1);
        }
    }

    function uncheckBlur(element) {
        element.style.filter = 'none';
    }

    function blurEvent(element) {
        element.style.filter = 'blur(10px)';
    }
});