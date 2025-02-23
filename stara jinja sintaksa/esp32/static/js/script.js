window.onload = function() {
   let element =  document.getElementById("dialog");

        if (element === null) {
            console.log("uspesno logovanje ili startovanje aplikacije");
        } else {
            element.showModal();
            setTimeout(() => {
                element.close();  // Zatvara modal posle 3 sekunde
            }, 3000);
        }
};