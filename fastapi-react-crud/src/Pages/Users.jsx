import React, { useState, useEffect } from "react";
import axios from "axios";

const Users = () => {
    const [users, setUsers] = useState([]);
    const [formData, setFormData] = useState({ username: "", email: "", password: "" });
    const [editingUser, setEditingUser] = useState(null);

    // Получение списка пользователей с сервера
    const fetchUsers = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/users");
            setUsers(response.data);
        } catch (error) {
            console.error("Ошибка при получении списка пользователей:", error);
        }
    };

    // Создание нового пользователя
    const createUser = async (e) => {
        e.preventDefault();
        try {
            await axios.post("http://127.0.0.1:8000/users/create", formData);
            fetchUsers();
            setFormData({ username: "", email: "", password: "" });
        } catch (error) {
            console.error("Ошибка при создании пользователя:", error);
        }
    };

    // Удаление пользователя
    const deleteUser = async (userId) => {
        try {
            await axios.delete(`http://127.0.0.1:8000/users/delete/${userId}`);
            fetchUsers();
        } catch (error) {
            console.error("Ошибка при удалении пользователя:", error);
        }
    };

    // Подготовка к редактированию пользователя
    const startEditing = (user) => {
        setEditingUser(user);
        setFormData({ username: user.username, email: user.email, password: "" });
    };

    // Завершение редактирования пользователя
    const updateUser = async (e) => {
        e.preventDefault();
        if (!editingUser) return;

        try {
            await axios.put(`http://127.0.0.1:8000/users/update/${editingUser.id}`, formData);
            fetchUsers();
            setEditingUser(null);
            setFormData({ username: "", email: "", password: "" });
        } catch (error) {
            console.error("Ошибка при обновлении пользователя:", error);
        }
    };

    // Отмена редактирования
    const cancelEditing = () => {
        setEditingUser(null);
        setFormData({ username: "", email: "", password: "" });
    };

    useEffect(() => {
        fetchUsers();
    }, []);

    return (
        <div>
            <h1>Управление пользователями</h1>

            <form onSubmit={editingUser ? updateUser : createUser}>
                <input
                    type="text"
                    placeholder="Username"
                    value={formData.username}
                    onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                    required
                />
                <input
                    type="email"
                    placeholder="Email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    required={!editingUser}
                />
                <button type="submit">{editingUser ? "Сохранить изменения" : "Добавить пользователя"}</button>
                {editingUser && <button onClick={cancelEditing}>Отмена</button>}
            </form>

            <ul>
                {users.map((user) => (
                    <li key={user.id}>
                        <strong>{user.username}</strong> - {user.email}
                        <button onClick={() => startEditing(user)}>Редактировать</button>
                        <button onClick={() => deleteUser(user.id)}>Удалить</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Users;
