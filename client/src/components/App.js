import { Routes, Route } from 'react-router-dom';
import Header from './Header';
import Vendor from './Vendor';
import Home from './Home';

function App() {
  return (
    <>
      <Header />
      <Routes>
        <Route path="/vendors/:id" element={<Vendor />} />
        <Route path="/" element={<Home />} />
      </Routes>
    </>
  );
}

export default App;
