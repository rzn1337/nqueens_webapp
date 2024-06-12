document.addEventListener('DOMContentLoaded', function() {
    function initPage(algorithm) {
        const canvas = document.getElementById('board-canvas');
        const context = canvas.getContext('2d');
        const NInput = document.getElementById('input-n');
        const toast = document.getElementById('toast-message');
        let N = parseInt(NInput.value);

        NInput.addEventListener('input', function() {
            const value = parseInt(this.value);
            if (!isNaN(value) && value >= 4) {
                N = value;
                resetBoard();
            } else {
                showToast('Please enter a valid number greater than or equal to 4');
            }
        });

        function drawBoard(board) {
            const cellSize = canvas.width / N;
            context.clearRect(0, 0, canvas.width, canvas.height);

            for (let row = 0; row < N; row++) {
                for (let col = 0; col < N; col++) {
                    context.fillStyle = (row + col) % 2 === 0 ? '#ffffff' : '#fcd8dc';
                    context.fillRect(col * cellSize, row * cellSize, cellSize, cellSize);
                }
            }

            const attacks = calculateAttacks(board);
            for (let row = 0; row < board.length; row++) {
                context.fillStyle = attacks[row] > 0 ? '#ff0000' : '#000000';
                context.beginPath();
                context.arc(board[row] * cellSize + cellSize / 2, row * cellSize + cellSize / 2, cellSize / 3, 0, 2 * Math.PI);
                context.fill();

                if (attacks[row] > 0) {
                    for (let col = 0; col < board.length; col++) {
                        if (col !== row && (board[col] === board[row] || Math.abs(board[col] - board[row]) === Math.abs(col - row))) {
                            context.strokeStyle = '#ff0000';
                            context.beginPath();
                            context.moveTo(board[row] * cellSize + cellSize / 2, row * cellSize + cellSize / 2);
                            context.lineTo(board[col] * cellSize + cellSize / 2, col * cellSize + cellSize / 2);
                            context.stroke();
                        }
                    }
                }
            }
        }

        function calculateAttacks(board) {
            const attacks = new Array(board.length).fill(0);
            for (let i = 0; i < board.length; i++) {
                for (let j = i + 1; j < board.length; j++) {
                    if (board[i] === board[j] || 
                        board[i] - i === board[j] - j || 
                        board[i] + i === board[j] + j) {
                        attacks[i]++;
                        attacks[j]++;
                    }
                }
            }
            return attacks;
        }

        function resetBoard() {
            context.clearRect(0, 0, canvas.width, canvas.height);
        }

        function showToast(message) {
            toast.textContent = message;
            toast.classList.remove('hidden');
            toast.style.opacity = 1;

            setTimeout(() => {
                toast.style.opacity = 0;
                setTimeout(() => toast.classList.add('hidden'), 300);
            }, 3000);
        }

        function showSpinner() {
            document.getElementById('loading-spinner').classList.remove('hidden');
        }

        function hideSpinner() {
            document.getElementById('loading-spinner').classList.add('hidden');
        }

        document.getElementById('btn-solve').addEventListener('click', function() {
            const value = parseInt(NInput.value);
            if (!isNaN(value) && value >= 4) {
                N = value;
                resetBoard();
                showSpinner();
                fetch('/find_solution', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ algorithm: algorithm, N: N })
                })
                .then(response => response.json())
                .then(data => {
                    hideSpinner();
                    if (data.success) {
                        drawBoard(data.board);
                    } else {
                        drawBoard(data.board);
                        showToast('Solution is incorrect');
                    }
                })
                .catch(error => {
                    hideSpinner();
                    showToast('An error occurred');
                    console.error('Error:', error);
                });
            } else {
                showToast('Please enter a valid number greater than or equal to 4');
            }
        });
    }

    // Export initPage function for each algorithm-specific page
    window.initPage = initPage;
});
