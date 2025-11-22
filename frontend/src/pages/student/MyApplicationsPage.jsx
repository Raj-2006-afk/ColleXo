import { useState, useEffect } from "react";
import DashboardLayout from "../../components/Layout/DashboardLayout";
import StatusPill from "../../components/StatusPill";
import axiosClient from "../../api/axiosClient";

const MyApplicationsPage = () => {
	const [applications, setApplications] = useState([]);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		fetchApplications();
	}, []);

	const fetchApplications = async () => {
		try {
			const response = await axiosClient.get("/applications/my-applications");
			setApplications(response.data.applications || []);
		} catch (error) {
			console.error("Error fetching applications:", error);
		} finally {
			setLoading(false);
		}
	};

	return (
		<DashboardLayout>
			<div className="max-w-7xl">
				<div className="mb-8">
					<h1 className="text-3xl font-bold text-gray-900 mb-2">
						My Applications
					</h1>
					<p className="text-gray-600">Track your society applications</p>
				</div>

				{loading ? (
					<div className="text-center py-12">
						<div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
					</div>
				) : applications.length > 0 ? (
					<div className="card overflow-hidden p-0">
						<table className="w-full">
							<thead className="bg-gray-50 border-b border-gray-200">
								<tr>
									<th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
										Society
									</th>
									<th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
										Form
									</th>
									<th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
										Submitted
									</th>
									<th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
										Status
									</th>
								</tr>
							</thead>
							<tbody className="bg-white divide-y divide-gray-200">
								{applications.map((app) => (
									<tr key={app.application_id}>
										<td className="px-6 py-4 whitespace-nowrap">
											<div className="font-medium text-gray-900">
												{app.society_name}
											</div>
										</td>
										<td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
											{app.form_title}
										</td>
										<td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
											{new Date(app.submitted_at).toLocaleDateString()}
										</td>
										<td className="px-6 py-4 whitespace-nowrap">
											<StatusPill status={app.status} />
										</td>
									</tr>
								))}
							</tbody>
						</table>
					</div>
				) : (
					<div className="card text-center text-gray-500 py-12">
						You haven't submitted any applications yet
					</div>
				)}
			</div>
		</DashboardLayout>
	);
};

export default MyApplicationsPage;
