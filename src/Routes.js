import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router";
import CSVUploader from "./Drag";
import Truck from "./Components/Truck";
import AllTrucks from "./AllTrucks";


const CustomRoute = (
    <BrowserRouter>
        <Routes>
            <Route path="/drag" element={<CSVUploader />} />
            <Route path="/truck" element={<Truck />} />
            <Route path="/AllTrucks" element={< AllTrucks />} />
        </Routes>
    </BrowserRouter>
)

export default CustomRoute