const pdfInput = document.getElementById("pdf");
const fileName = document.getElementById("file-name");
const chooseBtn = document.querySelector(".choose-btn");

if (pdfInput && fileName && chooseBtn) {

    pdfInput.addEventListener("change", function () {

        if (this.files.length > 0) {

            fileName.innerHTML = "✅ " + this.files[0].name;

            chooseBtn.classList.add("file-selected");
            chooseBtn.innerHTML = "✅ PDF Selected";

        } else {

            fileName.innerHTML = "Select PDF file";

            chooseBtn.classList.remove("file-selected");
            chooseBtn.innerHTML = "📄 Choose PDF";

        }

    });

}