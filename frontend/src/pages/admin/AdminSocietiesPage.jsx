import { useState, useEffect } from "react";
import DashboardLayout from "../../components/Layout/DashboardLayout";
import axiosClient from "../../api/axiosClient";

const AdminSocietiesPage = () => {
	const [societies, setSocieties] = useState([]);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		fetchSocieties();
	}, []);

	const fetchSocieties = async () => {
		try {
			const response = await axiosClient.get("/admin/societies");
			setSocieties(response.data.societies || []);
		} catch (error) {
			console.error("Error fetching societies:", error);
		} finally {
			setLoading(false);
		}
	};

	const toggleAdmission = async (societyId, currentStatus) => {
		try {
			await axiosClient.put(`/admin/societies/${societyId}/approve`, {
				approve: !currentStatus,
			});
			fetchSocieties();
		} catch (error) {
			alert("Failed to update society");
		}
	};

	return (
		<DashboardLayout>
			<div className="max-w-7xl">
				<h1 className="text-3xl font-bold text-gray-900 mb-8">
					Manage Societies
				</h1>

				{loading ? (
					<div className="text-center py-12">
						<div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
					</div>
				) : societies.length > 0 ? (
					<div className="card overflow-hidden p-0">
						<table className="w-full">
							<thead className="bg-gray-50 border-b">
								<tr>
									<th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
										Name
									</th>
									<th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
										Category
									</th>
									<th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
										Head
									</th>
									<th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
										Members
									</th>
									<th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
										Status
									</th>
									<th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
										Actions
									</th>
								</tr>
							</thead>
							<tbody className="divide-y">
								{societies.map((society) => (
									<tr key={society.society_id}>
										<td className="px-6 py-4 font-medium">
											{society.society_name}
										</td>
										<td className="px-6 py-4 text-sm text-gray-600">
											{society.category}
										</td>
										<td className="px-6 py-4 text-sm text-gray-600">
											{society.head_name || "N/A"}
										</td>
										<td className="px-6 py-4 text-sm text-gray-600">
											{society.member_count}
										</td>
										<td className="px-6 py-4">
											<span
												className={`px-3 py-1 rounded-full text-xs font-medium ${
													society.admission_open
														? "bg-green-100 text-green-700"
														: "bg-gray-100 text-gray-700"
												}`}
											>
												{society.admission_open ? "Open" : "Closed"}
											</span>
										</td>
										<td className="px-6 py-4">
											<button
												onClick={() =>
													toggleAdmission(
														society.society_id,
														society.admission_open
													)
												}
												className="text-primary-600 hover:text-primary-700 text-sm font-medium"
											>
												{society.admission_open ? "Close" : "Open"} Admission
											</button>
										</td>
									</tr>
								))}
							</tbody>
						</table>
					</div>
				) : (
					<div className="card text-center text-gray-500 py-12">
						No societies found
					</div>
				)}
			</div>
		</DashboardLayout>
	);
};

export default AdminSocietiesPage;
