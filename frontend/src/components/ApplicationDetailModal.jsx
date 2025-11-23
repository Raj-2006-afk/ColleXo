import { useState, useEffect } from "react";
import axiosClient from "../api/axiosClient";

const ApplicationDetailModal = ({ applicationId, onClose, onStatusUpdate }) => {
	const [application, setApplication] = useState(null);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		fetchApplicationDetails();
	}, [applicationId]);

	const fetchApplicationDetails = async () => {
		try {
			const response = await axiosClient.get(`/applications/${applicationId}`);
			setApplication(response.data);
		} catch (error) {
			console.error("Error fetching application details:", error);
		} finally {
			setLoading(false);
		}
	};

	const handleStatusChange = async (newStatus) => {
		try {
			await axiosClient.put(`/applications/${applicationId}/status`, {
				status: newStatus,
			});
			onStatusUpdate();
			onClose();
		} catch (error) {
			alert("Failed to update status");
		}
	};

	const getStatusColor = (status) => {
		switch (status) {
			case "pending":
				return "bg-yellow-100 text-yellow-800";
			case "shortlisted":
				return "bg-blue-100 text-blue-800";
			case "accepted":
				return "bg-green-100 text-green-800";
			case "rejected":
				return "bg-red-100 text-red-800";
			default:
				return "bg-gray-100 text-gray-800";
		}
	};

	if (loading) {
		return (
			<div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
				<div className="bg-white rounded-lg p-8">
					<div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
				</div>
			</div>
		);
	}

	if (!application) {
		return null;
	}

	return (
		<div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
			<div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
				{/* Header */}
				<div className="sticky top-0 bg-white border-b px-6 py-4 flex justify-between items-center">
					<div>
						<h2 className="text-2xl font-bold text-gray-900">
							Application Details
						</h2>
						<p className="text-sm text-gray-600 mt-1">
							{application.form_title}
						</p>
					</div>
					<button
						onClick={onClose}
						className="text-gray-400 hover:text-gray-600"
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

				{/* Content */}
				<div className="p-6">
					{/* Applicant Info */}
					<div className="bg-gray-50 rounded-lg p-4 mb-6">
						<h3 className="text-lg font-semibold text-gray-900 mb-3">
							Applicant Information
						</h3>
						<div className="grid md:grid-cols-2 gap-4">
							<div>
								<p className="text-sm text-gray-600">Name</p>
								<p className="font-medium text-gray-900">
									{application.user_name}
								</p>
							</div>
							<div>
								<p className="text-sm text-gray-600">Email</p>
								<p className="font-medium text-gray-900">
									{application.user_email}
								</p>
							</div>
							<div>
								<p className="text-sm text-gray-600">Submitted</p>
								<p className="font-medium text-gray-900">
									{new Date(application.submitted_at).toLocaleDateString()}
								</p>
							</div>
							<div>
								<p className="text-sm text-gray-600">Current Status</p>
								<span
									className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(
										application.status
									)}`}
								>
									{application.status.charAt(0).toUpperCase() +
										application.status.slice(1)}
								</span>
							</div>
						</div>
					</div>

					{/* Responses */}
					<div className="space-y-6">
						<h3 className="text-lg font-semibold text-gray-900">
							Application Responses
						</h3>
						{application.responses && application.responses.length > 0 ? (
							application.responses.map((response, index) => (
								<div
									key={response.response_id}
									className="border-l-4 border-primary-500 pl-4 py-2"
								>
									<p className="text-sm font-medium text-gray-700 mb-2">
										{index + 1}. {response.question_text}
									</p>
									<p className="text-gray-900 whitespace-pre-wrap">
										{response.response_text || (
											<span className="text-gray-400 italic">No response</span>
										)}
									</p>
								</div>
							))
						) : (
							<p className="text-gray-500 italic">No responses recorded</p>
						)}
					</div>
				</div>

				{/* Footer - Actions */}
				<div className="sticky bottom-0 bg-gray-50 border-t px-6 py-4">
					<div className="flex justify-between items-center">
						<p className="text-sm text-gray-600">Update application status:</p>
						<div className="flex space-x-2">
							<button
								onClick={() => handleStatusChange("shortlisted")}
								disabled={application.status === "shortlisted"}
								className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
							>
								Shortlist
							</button>
							<button
								onClick={() => handleStatusChange("accepted")}
								disabled={application.status === "accepted"}
								className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
							>
								Accept
							</button>
							<button
								onClick={() => handleStatusChange("rejected")}
								disabled={application.status === "rejected"}
								className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed"
							>
								Reject
							</button>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
};

export default ApplicationDetailModal;
