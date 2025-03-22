const products = JSON.parse(document.getElementById('products-data').textContent);
console.log(products);
const productNames = products.map(product => product[0]);
const productQuantities = products.map(product => product[1]);

console.log(productNames);
console.log(productQuantities);
const ctx = document.getElementById('productChart').getContext('2d');
const productChart = new Chart(ctx, {
    type: 'bar', 
    data: {
        labels: productNames,
        datasets: [{
            title: 'Product Quantities',
            label: 'Quantity',
            data: productQuantities,
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
                    text: "Quantity" 
                }
            },
            x: {
                title: {
                    display: true,
                    text: "Products" 
                }
            }
        }
        }
});
