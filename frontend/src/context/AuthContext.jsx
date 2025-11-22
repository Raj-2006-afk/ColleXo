import { createContext, useState, useEffect } from "react";
import axiosClient from "../api/axiosClient";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
	const [user, setUser] = useState(null);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		const storedUser = localStorage.getItem("user");
		const token = localStorage.getItem("token");

		if (storedUser && token) {
			setUser(JSON.parse(storedUser));
		}
		setLoading(false);
	}, []);

	const login = async (email, password) => {
		try {
			const response = await axiosClient.post("/auth/login", {
				user_email: email,
				user_password: password,
			});

			const { token, user } = response.data;

			localStorage.setItem("token", token);
			localStorage.setItem("user", JSON.stringify(user));
			setUser(user);

			return { success: true, user };
		} catch (error) {
			return {
				success: false,
				error: error.response?.data?.error || "Login failed",
			};
		}
	};

	const register = async (name, email, password, role = "student") => {
		try {
			const response = await axiosClient.post("/auth/register", {
				user_name: name,
				user_email: email,
				user_password: password,
				user_role: role,
			});

			const { token, user } = response.data;

			localStorage.setItem("token", token);
			localStorage.setItem("user", JSON.stringify(user));
			setUser(user);

			return { success: true, user };
		} catch (error) {
			return {
				success: false,
				error: error.response?.data?.error || "Registration failed",
			};
		}
	};

	const logout = () => {
		localStorage.removeItem("token");
		localStorage.removeItem("user");
		setUser(null);
		window.location.href = "/";
	};

	const value = {
		user,
		login,
		register,
		logout,
		loading,
		isAuthenticated: !!user,
	};

	return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
