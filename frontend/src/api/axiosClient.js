import axios from "axios";

const axiosClient = axios.create({
	baseURL: "http://localhost:5000/api",
	headers: {
		"Content-Type": "application/json",
	},
});

axiosClient.interceptors.request.use(
	(config) => {
		const token = localStorage.getItem("token");
		if (token) {
			config.headers.Authorization = `Bearer ${token}`;
		}
		return config;
	},
	(error) => {
		return Promise.reject(error);
	}
);

axiosClient.interceptors.response.use(
	(response) => response,
	(error) => {
		// Debug logging with persistent storage
		const errorInfo = {
			status: error.response?.status,
			data: error.response?.data,
			url: error.response?.config?.url,
			timestamp: new Date().toISOString(),
		};

		console.error("🔴 API Error:", errorInfo);

		// Store in sessionStorage so it persists across redirects
		const existingErrors = JSON.parse(
			sessionStorage.getItem("debug_errors") || "[]"
		);
		existingErrors.push(errorInfo);
		sessionStorage.setItem(
			"debug_errors",
			JSON.stringify(existingErrors.slice(-5))
		); // Keep last 5

		// Only logout on actual authentication/token failures (401)
		if (error.response && error.response.status === 401) {
			const errorMsg = error.response.data?.error?.toLowerCase() || "";
			const errorMessage = error.response.data?.message?.toLowerCase() || "";

			const isTokenError =
				errorMsg.includes("token") ||
				errorMsg.includes("authentication") ||
				errorMsg.includes("unauthorized") ||
				errorMessage.includes("token") ||
				errorMessage.includes("jwt") ||
				errorMessage.includes("expired");

			console.error(
				"🔴 Would logout:",
				isTokenError,
				"Error:",
				errorMsg,
				errorMessage
			);

			if (isTokenError) {
				localStorage.removeItem("token");
				localStorage.removeItem("user");
				window.location.href = "/login";
			}
		}
		return Promise.reject(error);
	}
);

export default axiosClient;
