import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axiosClient from "../api/axiosClient";

const NotificationBanner = () => {
	const [newForms, setNewForms] = useState([]);
	const [showBanner, setShowBanner] = useState(false);

	useEffect(() => {
		checkForNewForms();
	}, []);

	const checkForNewForms = async () => {
		try {
			const response = await axiosClient.get("/forms/published?per_page=3");
			const forms = response.data.forms || [];

			// Check if user has seen these forms
			const seenFormIds = JSON.parse(localStorage.getItem("seenForms") || "[]");
			const unseenForms = forms.filter(
				(form) => !seenFormIds.includes(form.form_id)
			);

			if (unseenForms.length > 0) {
				setNewForms(unseenForms);
				setShowBanner(true);
			}
		} catch (error) {
			console.error("Error checking for new forms:", error);
		}
	};

	const dismissBanner = () => {
		// Mark forms as seen
		const seenFormIds = JSON.parse(localStorage.getItem("seenForms") || "[]");
		const newSeenIds = [...seenFormIds, ...newForms.map((f) => f.form_id)];
		localStorage.setItem("seenForms", JSON.stringify(newSeenIds));
		setShowBanner(false);
	};

	if (!showBanner || newForms.length === 0) return null;

	return (
		<div className="bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-lg">
			<div className="max-w-7xl mx-auto px-4 py-4">
				<div className="flex items-center justify-between">
					<div className="flex items-center space-x-4">
						<div className="flex-shrink-0">
							<span className="text-2xl">🎯</span>
						</div>
						<div>
							<p className="font-semibold text-lg">
								🎉 New Recruitment Forms Available!
							</p>
							<p className="text-sm text-primary-100">
								{newForms.length}{" "}
								{newForms.length === 1 ? "society is" : "societies are"} now
								accepting applications
							</p>
						</div>
					</div>
					<div className="flex items-center space-x-3">
						<Link
							to="/student/forms"
							className="bg-white text-primary-600 px-6 py-2 rounded-lg font-semibold hover:bg-primary-50 transition-colors"
							onClick={dismissBanner}
						>
							View Forms
						</Link>
						<button
							onClick={dismissBanner}
							className="text-white hover:text-primary-100 transition-colors"
							aria-label="Dismiss notification"
						>
							<svg
								className="w-6 h-6"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									strokeLinecap="round"
									strokeLinejoin="round"
									strokeWidth={2}
									d="M6 18L18 6M6 6l12 12"
								/>
							</svg>
						</button>
					</div>
				</div>
			</div>
		</div>
	);
};

export default NotificationBanner;
