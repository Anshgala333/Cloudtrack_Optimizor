import React, { useEffect, useState } from 'react';
import { Canvas } from "@react-three/fiber";
import { OrbitControls, Stats } from "@react-three/drei";
import TruckView from './Components/Truck1';
import TruckDetails from './Components/TruckDetails';
import CustomerDetail from './Components/CustomerDetail';
import Unplaced from './Components/Unplaced';


export default function AllTrucks() {
    const fileName = "test5.csv";
    const fileName1 = "differentShape.csv";

    const [truck, setTruck] = useState([]);
    const [index, setIndex] = useState(0);
    const [customerSummary, setCustomerSummary] = useState([]);
    const [unplacedOrders, setUnplacedOrders] = useState([]);

    const selectedTruck = truck[index];
    const [showWeights, setShowWeights] = useState(false);



    useEffect(() => {
        async function getData() {
            try {
                // const response = await fetch(`${process.env.REACT_APP_API}/upload/getDataForThisCSV/boxOfSameSize/${fileName}`);
                const response = await fetch(`${process.env.REACT_APP_API}/upload/getDataForThisCSV/boxOfDifferentSize/${fileName1}`);
                const data = await response.json();
                setTruck(data.message.trucks);
                setUnplacedOrders(data.message.not_placed);
                setCustomerSummary(data.message.customer_summary);
                // console.log(data.message)
            } catch (e) {
                console.error("Error fetching truck data", e);
            }
        }
        getData();
    }, []);


    return (
        <div className='fullscreen-container'>

            {/* Top Left: Dropdown */}
            {truck.length > 1 && (
                <div style={{ position: "absolute", top: 10, left: 10, zIndex: 10 }}>
                    <select
                        value={index}
                        onChange={(e) => setIndex(parseInt(e.target.value))}
                        className='select-btn'
                    >
                        {truck.map((t, i) => (
                            <option key={i} value={i}>
                                Truck {i + 1} - {t.name || 'Unnamed Truck'}
                            </option>
                        ))}
                    </select>
                </div>
            )}
            <div style={{
                position: "absolute",
                left: "12%",
                top: 10,
                zIndex: 10
            }}>
                <button
                    onClick={() => setShowWeights(prev => !prev)}
                    className='primary-button '
                >
                    {showWeights ? 'Hide Row Weights' : 'Show Row Weights'}
                </button>
            </div>


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
                    <TruckView truck={selectedTruck} showWeights={showWeights} />
                    <OrbitControls enableZoom={true} />
                </Canvas>
            )}

            {/* custome color code middle right */}
            <CustomerDetail truck={truck} index={index} />

            {Object.keys(unplacedOrders).length > 0 && (
                <Unplaced unplacedOrders={unplacedOrders} />
            )}

            {customerSummary && customerSummary.length > 0 && (
                <div className="summary-panel">
                    <div className="summary-panel-title">📊 Customer Summary</div>
                    {customerSummary.map((item, idx) => (
                        <div key={idx} className="summary-row">
                            <span className="summary-customer">🧍 {item.customer_name}</span>
                            <span className="summary-priority">Priority {item.priority}</span>
                            <span className="summary-boxes">Boxes: {item.total_boxes}</span>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
