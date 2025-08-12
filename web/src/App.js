import { Routes, Route, BrowserRouter } from "react-router-dom";
import HomePage from './HomePage';
import UserPage from './UserPage';
import AdminPage from './AdminPage';
import InsertPage from './InsertPage';
import EditPost from "./EditPost";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route index element={<HomePage />} />
        <Route path="user" element={<UserPage />} />
        <Route path="admin" element={<AdminPage />} />
        <Route path="insert" element={<InsertPage />} />
        <Route path="/edit/:postId" element={<EditPost />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
