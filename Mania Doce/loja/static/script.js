'use strict';
const idade = document.getElementById("idade");
const erroIdade = document.getElementById("erroIdade");
const email = document.getElementById("email");
const user = document.getElementById("user");
const senha = document.getElementById("senha");

idade.addEventListener('input', () => {
    validarIdade(idade.value);
});
function validarIdade(valor) {
    const idadeNum = Number(valor);

    if (isNaN(idadeNum) || idadeNum < 18) {
        erroIdade.style.display = 'block';
    } else {
        erroIdade.style.display = 'none';
    }
};

