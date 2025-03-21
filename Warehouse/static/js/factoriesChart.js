        // Retrieve the serialized products data
        const factories = JSON.parse(document.getElementById('factory-data').textContent);
        console.log(factories);
        const factoryNames = factories.map(factory => factory['name']);
        const factoryShipment = factories.map(factory => factory['total_shipments']);
    
        console.log(factoryNames);
        console.log(factoryShipment);
        const ctx2 = document.getElementById('factoryChart').getContext('2d');
        const factoryChart = new Chart(ctx2, {
            type: 'bar', 
            data: {
                labels: factoryNames,
                datasets: [{
                    label: 'Shipments',
                    data: factoryShipment,
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
                            text: "Total Shipments" 
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: "Factories" 
                        }
                    }
                }
                }
            });
    