import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";

// PAGES IMPORT
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import PageNotFound from "./pages/PageNotFound";

// COMPONENTS IMPORT
// import Header from "./components/Header";
// import Footer from "./components/Footer";

function App() {
  return (
    <Router>
      {/* <Header /> */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/*" element={<PageNotFound />} />
      </Routes>
      {/* <Footer /> */}
    </Router>
  );
}

export default App;
