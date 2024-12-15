import React from "react";
import Users from "./Pages/Users";
import Posts from "./Pages/Posts";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/users" element={<Users />} />
                <Route path="/posts" element={<Posts />} />
            </Routes>
        </Router>
    );
}

export default App;