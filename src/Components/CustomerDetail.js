import React from 'react'

export default function CustomerDetail({ truck, index }) {
    console.log(truck)
    const selectedTruck = truck[index]

    function extractCustomerInfo(truck) {
        const PRIORITY_COLORS = {
            1: "#FFA500", // Orange
            2: "#87CEEB", // Sky Blue
            3: "#34D399", // Green
            4: "#f472b6", // Pink
        };

        const map = new Map();
        truck.boxes.forEach((box) => {
            const key = box.customer_name;
            if (!map.has(key)) {
                map.set(key, { priority: box.priority, count: 0 });
            }
            map.get(key).count += 1;
        });

        return Array.from(map.entries()).map(([customer, data]) => ({
            customer,
            count: data.count,
            priority: data.priority,
            color: PRIORITY_COLORS[data.priority] || "#999",
        }));
    }
    const customerInfo = selectedTruck ? extractCustomerInfo(selectedTruck) : [];
    return (

        <>
            {customerInfo && customerInfo.length > 0 && <div>
                <div className="customer-panel">
                    <div className="customer-panel-title">📦 Customers in this Truck</div>
                    {customerInfo.map((info) => (
                        <div key={info.customer} className="customer-row">
                            <div className="color-badge" style={{ backgroundColor: info.color }}></div>
                            <div className="customer-name">{info.customer}</div>
                            <div className="customer-name"> priority {info.priority}</div>
                            <div className="box-count">× {info.count}</div>
                        </div>
                    ))}
                </div>
            </div>}

        </>

    )
}
