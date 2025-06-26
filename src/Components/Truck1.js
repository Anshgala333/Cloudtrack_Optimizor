import { Canvas } from "@react-three/fiber";
import { OrbitControls, Stats, Edges } from "@react-three/drei";
import * as THREE from "three";
import React, { useMemo } from "react";
import { Html } from "@react-three/drei"; // For floating legend panel


// Box dimensions
const BOX_LENGTH = 0.46;
const BOX_WIDTH = 0.46;
const BOX_HEIGHT = 0.41;

// Priority-color map
const PRIORITY_COLORS = {
  1: "#FFA500", // Orange
  2: "#87CEEB", // Sky Blue
  3: "#34D399", // Green
  4: "#f472b6", // Pink
};

function DetailedWheel({ position }) {
  return (
    <group position={position} rotation={[0, 0, Math.PI / 2]}>
      <mesh>
        <cylinderGeometry args={[0.3, 0.3, 0.2, 32]} />
        <meshStandardMaterial color="#111" metalness={0.6} roughness={0.4} />
      </mesh>
      <mesh>
        <cylinderGeometry args={[0.2, 0.2, 0.21, 32]} />
        <meshStandardMaterial color="#9ca3af" metalness={0.8} roughness={0.2} />
      </mesh>
      <mesh>
        <cylinderGeometry args={[0.05, 0.05, 0.22, 16]} />
        <meshStandardMaterial color="#e5e7eb" metalness={0.5} roughness={0.1} />
      </mesh>
    </group>
  );
}

export default function TruckView({ truck }) {
  const truckData = [
    { name: "12-ft Truck", length: 3.66, width: 2.0, height: 2.0, max_weight: 3000 },
    { name: "24-ft Truck", length: 7.32, width: 2.44, height: 2.6, max_weight: 8000 },
    { name: "32-ft Truck", length: 9.75, width: 2.44, height: 2.6, max_weight: 10000 },
  ];
  const selectedTruck = truckData.find((t) => t.name === truck.name);
  const TRUCK_LENGTH = selectedTruck.length;
  const TRUCK_WIDTH = selectedTruck.width;
  const TRUCK_HEIGHT = selectedTruck.height;

  // Group boxes by customer with color for each priority
  var id = truck.boxes.map((e) => e.custom_id)
  console.log(id)


  return (
    <>
      {/* Truck 3D View */}
      <group>
        {/* Transparent container */}
        <mesh position={[TRUCK_WIDTH / 2, TRUCK_HEIGHT / 2, TRUCK_LENGTH / 2]}>
          <boxGeometry args={[TRUCK_WIDTH, TRUCK_HEIGHT, TRUCK_LENGTH]} />
          <meshStandardMaterial color="#cccccc" transparent opacity={0.1} side={THREE.DoubleSide} />
          <Edges scale={1.01} color="#444" />
        </mesh>

        {/* Wheels */}
        {[0.3, 1.7].map((x, i) => (
          <React.Fragment key={i}>
            {/* front wheel */}
            <DetailedWheel position={[x, -0.25, -0.5]} />

            {/* rear wheel */}
            <DetailedWheel position={[x, -0.3, TRUCK_LENGTH - 0.5]} />
          </React.Fragment>
        ))}

        {/* Boxes */}
        {truck.boxes.map((box, idx) => (

          <group
            key={box.custom_id}
            position={[
              box.position.x + BOX_WIDTH / 2,
              box.position.z + BOX_HEIGHT / 2,
              box.position.y + BOX_LENGTH / 2,
            ]}
          >
            <mesh>
              <boxGeometry args={[BOX_WIDTH, BOX_HEIGHT, BOX_LENGTH]} />
              <meshStandardMaterial
                color={PRIORITY_COLORS[box.priority] || "#999"}
                roughness={0.4}
                metalness={0.1}
              />
              <Edges scale={1.03} color="#111" />
            </mesh>
          </group>
        ))}

        {/* Front Cab */}
        <group position={[TRUCK_WIDTH / 2, TRUCK_HEIGHT / 4, -0.5]}>
          <mesh>
            <boxGeometry args={[TRUCK_WIDTH * 0.9, TRUCK_HEIGHT * 0.5, 1.0]} />
            <meshStandardMaterial color="red" metalness={0.5} roughness={0.2} />
          </mesh>
        </group>
      </group>

      {/* Customer Color Panel (Legend) */}
    </>
  );
}
