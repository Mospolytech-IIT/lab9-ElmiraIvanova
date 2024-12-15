import React, { useState, useEffect } from "react";
import axios from "axios";

const Posts = () => {
    const [posts, setPosts] = useState([]);
    const [formData, setFormData] = useState({ title: "", content: "", user_id: "" });
    const [editingPost, setEditingPost] = useState(null);

    const fetchPosts = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/posts");
            setPosts(response.data);
        } catch (error) {
            console.error("Ошибка при получении списка постов:", error);
        }
    };

    const createPost = async (e) => {
        e.preventDefault();
        try {
            await axios.post("http://127.0.0.1:8000/posts/create", formData, {
                headers: { "Content-Type": "application/json" },
            });
            fetchPosts();
            setFormData({ title: "", content: "", user_id: "" });
        } catch (error) {
            console.error("Ошибка при создании поста:", error);
        }
    };

    const deletePost = async (postId) => {
        try {
            await axios.delete(`http://127.0.0.1:8000/posts/delete/${postId}`);
            fetchPosts();
        } catch (error) {
            console.error("Ошибка при удалении поста:", error);
        }
    };

    const startEditing = (post) => {
        setEditingPost(post);
        setFormData({ title: post.title, content: post.content, user_id: post.user_id });
    };

    const updatePost = async (e) => {
        e.preventDefault();
        if (!editingPost) return;

        try {
            await axios.put(`http://127.0.0.1:8000/posts/update/${editingPost.id}`, formData, {
                headers: { "Content-Type": "application/json" },
            });
            fetchPosts();
            setEditingPost(null);
            setFormData({ title: "", content: "", user_id: "" });
        } catch (error) {
            console.error("Ошибка при обновлении поста:", error);
        }
    };

    const cancelEditing = () => {
        setEditingPost(null);
        setFormData({ title: "", content: "", user_id: "" });
    };

    useEffect(() => {
        fetchPosts();
    }, []);

    return (
        <div>
            <h1>Управление постами</h1>

            <form onSubmit={editingPost ? updatePost : createPost}>
                <input
                    type="text"
                    placeholder="Title"
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    required
                />
                <textarea
                    placeholder="Content"
                    value={formData.content}
                    onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                    required
                />
                <input
                    type="number"
                    placeholder="User ID"
                    value={formData.user_id}
                    onChange={(e) => setFormData({ ...formData, user_id: e.target.value })}
                    required
                />
                <button type="submit">{editingPost ? "Сохранить изменения" : "Добавить пост"}</button>
                {editingPost && <button onClick={cancelEditing}>Отмена</button>}
            </form>

            <ul>
                {posts.map((post) => (
                    <li key={post.id}>
                        <strong>{post.title}</strong> - {post.content}
                        <button onClick={() => startEditing(post)}>Редактировать</button>
                        <button onClick={() => deletePost(post.id)}>Удалить</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Posts;
