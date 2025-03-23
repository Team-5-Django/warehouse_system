const supermarkets = JSON.parse(document.getElementById('supermarket-data').textContent);
console.log(supermarkets);
const supermarketNames = supermarkets.map(factory => factory['name']);
const supermarketOrder = supermarkets.map(factory => factory['total_orders']);

console.log(supermarketNames);
console.log(supermarketOrder);
const ctx3 = document.getElementById('supermarketChart').getContext('2d');
const supermarketChart = new Chart(ctx3, {
    type: 'bar', 
    data: {
        labels: supermarketNames,
        datasets: [{
            label: 'Orders',
            data: supermarketOrder,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    stepSize: 1,  // 🟢 Force only integer steps
                    callback: function(value) {
                        return Number.isInteger(value) ? value : null;  // 🟢 Show only whole numbers
                    }
                },
                title: {
                    display: true,
                    text: "Total Orders" 
                }
            },
            x: {
                title: {
                    display: true,
                    text: "Supermarkets" 
                }
            }
        }
        }
    });
