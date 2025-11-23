import { useState, useEffect } from "react";
import DashboardLayout from "../../components/Layout/DashboardLayout";
import SocietyCard from "../../components/SocietyCard";
import NotificationBanner from "../../components/NotificationBanner";
import axiosClient from "../../api/axiosClient";

const StudentDashboard = () => {
	const [societies, setSocieties] = useState([]);
	const [applications, setApplications] = useState([]);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		fetchData();
	}, []);

	const fetchData = async () => {
		try {
			const [societiesRes, applicationsRes] = await Promise.all([
				axiosClient.get("/societies/browse?per_page=6&admission_open=true"),
				axiosClient.get("/applications/my-applications?per_page=5"),
			]);
			setSocieties(societiesRes.data.societies || []);
			setApplications(applicationsRes.data.applications || []);
		} catch (error) {
			console.error("Error fetching data:", error);
		} finally {
			setLoading(false);
		}
	};

	return (
		<DashboardLayout>
			<NotificationBanner />
			<div className="max-w-7xl">
				<div className="mb-8">
					<h1 className="text-3xl font-bold text-gray-900 mb-2">
						Student Dashboard
					</h1>
					<p className="text-gray-600">
						Explore societies and manage your applications
					</p>
				</div>

				<div className="mb-8">
					<h2 className="text-xl font-semibold text-gray-900 mb-4">
						Open for Applications
					</h2>
					{loading ? (
						<div className="text-center py-12">
							<div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
						</div>
					) : societies.length > 0 ? (
						<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
							{societies.map((society) => (
								<SocietyCard key={society.society_id} society={society} />
							))}
						</div>
					) : (
						<div className="card text-center text-gray-500 py-12">
							No societies currently accepting applications
						</div>
					)}
				</div>

				{applications.length > 0 && (
					<div className="mt-8">
						<h2 className="text-xl font-semibold text-gray-900 mb-4">
							My Recent Applications
						</h2>
						<div className="bg-white rounded-lg shadow overflow-hidden">
							<div className="divide-y">
								{applications.map((app) => (
									<div
										key={app.application_id}
										className="p-4 hover:bg-gray-50 transition-colors"
									>
										<div className="flex items-center justify-between">
											<div className="flex items-center space-x-4">
												{app.logo_url && (
													<img
														src={app.logo_url}
														alt={app.society_name}
														className="w-12 h-12 object-cover rounded-lg"
													/>
												)}
												<div>
													<h3 className="font-semibold text-gray-900">
														{app.society_name}
													</h3>
													<p className="text-sm text-gray-600">
														{app.form_title}
													</p>
													<p className="text-xs text-gray-500 mt-1">
														Submitted on{" "}
														{new Date(app.submitted_at).toLocaleDateString()}
													</p>
												</div>
											</div>
											<div>
												<span
													className={`px-3 py-1 rounded-full text-sm font-medium ${
														app.status === "pending"
															? "bg-yellow-100 text-yellow-800"
															: app.status === "shortlisted"
															? "bg-blue-100 text-blue-800"
															: app.status === "accepted"
															? "bg-green-100 text-green-800"
															: "bg-red-100 text-red-800"
													}`}
												>
													{app.status.charAt(0).toUpperCase() +
														app.status.slice(1)}
												</span>
											</div>
										</div>
									</div>
								))}
							</div>
						</div>
					</div>
				)}
			</div>
		</DashboardLayout>
	);
};

export default StudentDashboard;
