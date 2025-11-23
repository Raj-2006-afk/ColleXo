import { useState, useEffect } from "react";
import DashboardLayout from "../../components/Layout/DashboardLayout";
import StatusPill from "../../components/StatusPill";
import ApplicationDetailModal from "../../components/ApplicationDetailModal";
import axiosClient from "../../api/axiosClient";

const SHApplicationsPage = () => {
	const [applications, setApplications] = useState([]);
	const [society, setSociety] = useState(null);
	const [loading, setLoading] = useState(true);
	const [filter, setFilter] = useState("");
	const [selectedAppId, setSelectedAppId] = useState(null);

	useEffect(() => {
		fetchData();
	}, [filter]);

	const fetchData = async () => {
		try {
			const societyRes = await axiosClient.get("/societies/my-society");
			setSociety(societyRes.data.society);

			if (societyRes.data.society) {
				const params = filter ? `?status=${filter}` : "";
				const appsRes = await axiosClient.get(
					`/applications/society/${societyRes.data.society.society_id}${params}`
				);
				setApplications(appsRes.data.applications || []);
			}
		} catch (error) {
			console.error("Error fetching applications:", error);
		} finally {
			setLoading(false);
		}
	};

	const updateStatus = async (appId, newStatus) => {
		try {
			await axiosClient.put(`/applications/${appId}/status`, {
				status: newStatus,
			});
			fetchData();
		} catch (error) {
			alert("Failed to update status");
		}
	};

	return (
		<DashboardLayout>
			<div className="max-w-7xl">
				<div className="mb-8">
					<h1 className="text-3xl font-bold text-gray-900 mb-4">
						Applications
					</h1>
					<div className="flex space-x-2">
						<button
							onClick={() => setFilter("")}
							className={!filter ? "btn-primary" : "btn-secondary"}
						>
							All
						</button>
						<button
							onClick={() => setFilter("pending")}
							className={filter === "pending" ? "btn-primary" : "btn-secondary"}
						>
							Pending
						</button>
						<button
							onClick={() => setFilter("shortlisted")}
							className={
								filter === "shortlisted" ? "btn-primary" : "btn-secondary"
							}
						>
							Shortlisted
						</button>
						<button
							onClick={() => setFilter("accepted")}
							className={
								filter === "accepted" ? "btn-primary" : "btn-secondary"
							}
						>
							Accepted
						</button>
					</div>
				</div>

				{loading ? (
					<div className="text-center py-12">
						<div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
					</div>
				) : applications.length > 0 ? (
					<div className="card overflow-hidden p-0">
						<table className="w-full">
							<thead className="bg-gray-50 border-b">
								<tr>
									<th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
										Student
									</th>
									<th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
										Email
									</th>
									<th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
										Status
									</th>
									<th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
										Submitted
									</th>
									<th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
										Actions
									</th>
								</tr>
							</thead>
							<tbody className="divide-y">
								{applications.map((app) => (
									<tr key={app.application_id} className="hover:bg-gray-50">
										<td className="px-6 py-4 font-medium">{app.user_name}</td>
										<td className="px-6 py-4 text-sm text-gray-600">
											{app.user_email}
										</td>
										<td className="px-6 py-4">
											<StatusPill status={app.status} />
										</td>
										<td className="px-6 py-4 text-sm text-gray-600">
											{new Date(app.submitted_at).toLocaleDateString()}
										</td>
										<td className="px-6 py-4">
											<button
												onClick={() => setSelectedAppId(app.application_id)}
												className="text-primary-600 hover:text-primary-700 font-medium text-sm"
											>
												View Details
											</button>
										</td>
									</tr>
								))}
							</tbody>
						</table>
					</div>
				) : (
					<div className="card text-center text-gray-500 py-12">
						No applications found
					</div>
				)}

				{/* Application Detail Modal */}
				{selectedAppId && (
					<ApplicationDetailModal
						applicationId={selectedAppId}
						onClose={() => setSelectedAppId(null)}
						onStatusUpdate={fetchData}
					/>
				)}
			</div>
		</DashboardLayout>
	);
};

export default SHApplicationsPage;
