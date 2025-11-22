// Main JavaScript utilities

// Logout function
function logout() {
	localStorage.removeItem("token");
	localStorage.removeItem("user");
	window.location.href = "/login";
}

// Check if user is authenticated
function isAuthenticated() {
	const token = localStorage.getItem("token");
	return !!token;
}

// Get current user
function getCurrentUser() {
	const userStr = localStorage.getItem("user");
	return userStr ? JSON.parse(userStr) : null;
}

// Make API request with authentication
async function apiRequest(url, options = {}) {
	const token = localStorage.getItem("token");

	const headers = {
		"Content-Type": "application/json",
		...options.headers,
	};

	if (token) {
		headers["Authorization"] = `Bearer ${token}`;
	}

	const response = await fetch(url, {
		...options,
		headers,
	});

	if (response.status === 401) {
		// Token expired or invalid
		logout();
		return null;
	}

	return response;
}

// Format date
function formatDate(dateString) {
	const date = new Date(dateString);
	return date.toLocaleDateString("en-US", {
		year: "numeric",
		month: "long",
		day: "numeric",
	});
}

// Show notification
function showNotification(message, type = "info") {
	const notification = document.createElement("div");
	notification.className = `notification notification-${type}`;
	notification.textContent = message;

	document.body.appendChild(notification);

	setTimeout(() => {
		notification.classList.add("show");
	}, 100);

	setTimeout(() => {
		notification.classList.remove("show");
		setTimeout(() => {
			document.body.removeChild(notification);
		}, 300);
	}, 3000);
}

// Validate email
function validateEmail(email) {
	const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
	return re.test(email);
}

// Initialize page
document.addEventListener("DOMContentLoaded", () => {
	// Check authentication on protected pages
	const protectedPaths = ["/dashboard", "/student", "/society", "/admin"];
	const currentPath = window.location.pathname;

	if (protectedPaths.some((path) => currentPath.includes(path))) {
		if (!isAuthenticated()) {
			window.location.href = "/login";
		}
	}
});
