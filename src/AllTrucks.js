import React, { useEffect, useState } from 'react';
import { Canvas } from "@react-three/fiber";
import { OrbitControls, Stats } from "@react-three/drei";
import TruckView from './Components/Truck1';
import TruckDetails from './Components/TruckDetails';


export default function AllTrucks() {
    const fileName = "test6.csv";

    const [truck, setTruck] = useState([]);
    const [index, setIndex] = useState(0);
    const [unplacedOrders, setUnplacedOrders] = useState([]);




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


    useEffect(() => {
        async function getData() {
            try {
                const response = await fetch(`${process.env.REACT_APP_API}/upload/getDataForThisCSV/${fileName}`);
                const data = await response.json();
                setTruck(data.message.trucks);
                setUnplacedOrders(data.message.not_placed);
                // console.log(data.message)
            } catch (e) {
                console.error("Error fetching truck data", e);
            }
        }
        getData();
    }, []);

    const selectedTruck = truck[index];
    const customerInfo = selectedTruck ? extractCustomerInfo(selectedTruck) : [];


    return (
        <div style={{ width: "100vw", height: "100vh", overflow: "hidden", background: "#eaeaea", position: "relative" }}>

            {/* Top Left: Dropdown */}
            {truck.length > 1 && (
                <div style={{ position: "absolute", top: 10, left: 10, zIndex: 10 }}>
                    <select
                        value={index}
                        onChange={(e) => setIndex(parseInt(e.target.value))}
                        style={{
                            padding: "8px 12px",
                            fontSize: "14px",
                            borderRadius: "8px",
                            border: "1px solid #ccc",
                            backgroundColor: "#fff",
                            boxShadow: "0 2px 5px rgba(0,0,0,0.1)"
                        }}
                    >
                        {truck.map((t, i) => (
                            <option key={i} value={i}>
                                Truck {i + 1} - {t.name || 'Unnamed Truck'}
                            </option>
                        ))}
                    </select>
                </div>
            )}

            {/* Top Center: Info Text */}
            {truck.length > 0 && (
                <>
                    <div className="status-header">
                        <span>📂 File:</span>
                        <strong>{fileName}</strong>
                        <span className="separator">|</span>
                        <span>🚚 Truck:</span>
                        <strong>{index + 1} / {truck.length}</strong>
                    </div>
                </>
            )}

            {/* Top Right: Truck Details */}
            {selectedTruck && (
                <TruckDetails selectedTruck={selectedTruck} />
            )}


            {/* 3D Canvas */}
            {selectedTruck && (
                <Canvas camera={{ position: [6, 6, 6], fov: 45 }} shadows>
                    <ambientLight intensity={0.9} />
                    <directionalLight position={[10, 20, 10]} intensity={1} castShadow />
                    <TruckView truck={selectedTruck} />
                    <OrbitControls enableZoom={true} />
                </Canvas>
            )}

            {/* custome color code middle right */}
            {customerInfo && customerInfo.length > 0 &&
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
                </div>}

            {Object.keys(unplacedOrders).length > 0 && (
                <div className="unplaced-panel">
                    <div className="unplaced-panel-title">🚫 Unplaced Boxes Summary</div>
                    {Object.entries(unplacedOrders).map(([customer, boxes]) => (
                        <div key={customer} className="unplaced-row single-line">
                            <span className="unplaced-customer">🧍 {customer}</span>
                            <span className="unplaced-count">× {boxes.length}</span>
                            <span className="reason-text">Low priority or insufficient capacity</span>
                        </div>
                    ))}
                </div>
            )}

        </div>
    );
}
