document.addEventListener('DOMContentLoaded', function() {
    const faqQuestions = document.querySelectorAll('.faq-question');
    
    faqQuestions.forEach(question => {
        question.addEventListener('click', function() {
            const answer = this.nextElementSibling;
            
            this.classList.toggle('active');
            answer.classList.toggle('active');
            
            faqQuestions.forEach(otherQuestion => {
                if (otherQuestion !== this) {
                    otherQuestion.classList.remove('active');
                    otherQuestion.nextElementSibling.classList.remove('active');
                }
            });
        });
    });
    
    const form = document.querySelector('.recomendacion-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const edad = document.getElementById('edad').value;
            const peso = document.getElementById('peso').value;
            const altura = document.getElementById('altura').value;
            const dias = document.getElementById('dias_disponibles').value;
            
            if (!edad || !peso || !altura || !dias) {
                e.preventDefault();
                alert('Por favor, completa todos los campos');
                return false;
            }
            
            if (edad < 15 || edad > 100) {
                e.preventDefault();
                alert('La edad debe estar entre 15 y 100 años');
                return false;
            }
            
            if (peso < 30 || peso > 300) {
                e.preventDefault();
                alert('El peso debe estar entre 30 y 300 kg');
                return false;
            }
            
            if (altura < 1.0 || altura > 2.5) {
                e.preventDefault();
                alert('La altura debe estar entre 1.0 y 2.5 metros');
                return false;
            }
            
            if (dias < 1 || dias > 7) {
                e.preventDefault();
                alert('Los días disponibles deben estar entre 1 y 7');
                return false;
            }
        });
    }
});
