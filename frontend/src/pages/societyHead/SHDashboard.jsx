import { useState, useEffect } from "react";
import DashboardLayout from "../../components/Layout/DashboardLayout";
import StatCard from "../../components/StatCard";
import axiosClient from "../../api/axiosClient";

const SHDashboard = () => {
	const [society, setSociety] = useState(null);
	const [stats, setStats] = useState(null);
	const [loading, setLoading] = useState(true);
	const [editingMembers, setEditingMembers] = useState(false);
	const [memberCount, setMemberCount] = useState(0);

	useEffect(() => {
		fetchData();
	}, []);

	const fetchData = async () => {
		try {
			const societyRes = await axiosClient.get("/societies/my-society");
			setSociety(societyRes.data.society);

			if (societyRes.data.society) {
				const statsRes = await axiosClient.get(
					`/applications/statistics/${societyRes.data.society.society_id}`
				);
				setStats(statsRes.data);
			}
		} catch (error) {
			if (error.response && error.response.status === 404) {
				// No society assigned yet - this is normal for new users
				setSociety(null);
			} else {
				console.error("Error fetching data:", error);
			}
		} finally {
			setLoading(false);
		}
	};

	const updateMemberCount = async () => {
		try {
			await axiosClient.put(`/societies/${society.society_id}`, {
				member_count: memberCount,
			});
			setEditingMembers(false);
			fetchData();
		} catch (error) {
			alert("Failed to update member count");
		}
	};

	// Debug: Check for errors
	const debugErrors = JSON.parse(
		sessionStorage.getItem("debug_errors") || "[]"
	);

	return (
		<DashboardLayout>
			<div className="max-w-7xl">
				{debugErrors.length > 0 && (
					<div className="mb-4 p-4 bg-red-100 border border-red-300 rounded">
						<h3 className="font-bold text-red-800 mb-2">Debug Errors:</h3>
						<pre className="text-xs overflow-auto">
							{JSON.stringify(debugErrors, null, 2)}
						</pre>
						<button
							onClick={() => sessionStorage.removeItem("debug_errors")}
							className="mt-2 text-xs bg-red-600 text-white px-2 py-1 rounded"
						>
							Clear Errors
						</button>
					</div>
				)}

				<h1 className="text-3xl font-bold text-gray-900 mb-8">
					Society Overview
				</h1>

				{loading ? (
					<div className="text-center py-12">
						<div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
					</div>
				) : society ? (
					<>
						<div className="grid md:grid-cols-4 gap-6 mb-8">
							<StatCard
								title="Total Applications"
								value={stats?.total || 0}
								icon="📬"
								color="primary"
							/>
							<StatCard
								title="Pending"
								value={stats?.pending || 0}
								icon="⏳"
								color="yellow"
							/>
							<StatCard
								title="Shortlisted"
								value={stats?.shortlisted || 0}
								icon="✓"
								color="blue"
							/>
							<StatCard
								title="Accepted"
								value={stats?.accepted || 0}
								icon="✅"
								color="green"
							/>
						</div>

						<div className="card">
							<div className="flex justify-between items-start mb-4">
								<h2 className="text-xl font-semibold">
									{society.society_name}
								</h2>
								{!editingMembers && (
									<button
										onClick={() => {
											setMemberCount(society.member_count || 0);
											setEditingMembers(true);
										}}
										className="text-sm text-primary-600 hover:text-primary-700 font-medium"
									>
										Update Members
									</button>
								)}
							</div>
							<p className="text-gray-600 mb-4">{society.description}</p>

							{editingMembers ? (
								<div className="flex items-center space-x-3 mb-4">
									<label className="text-sm font-medium text-gray-700">
										Member Count:
									</label>
									<input
										type="number"
										min="0"
										value={memberCount}
										onChange={(e) =>
											setMemberCount(parseInt(e.target.value) || 0)
										}
										className="w-24 px-3 py-1 border border-gray-300 rounded"
									/>
									<button
										onClick={updateMemberCount}
										className="px-4 py-1 bg-primary-600 text-white rounded hover:bg-primary-700 text-sm"
									>
										Save
									</button>
									<button
										onClick={() => setEditingMembers(false)}
										className="px-4 py-1 border border-gray-300 rounded hover:bg-gray-50 text-sm"
									>
										Cancel
									</button>
								</div>
							) : (
								<div className="flex items-center space-x-4 text-sm text-gray-600">
									<span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full">
										{society.category}
									</span>
									<span className="font-medium">
										{society.member_count} members
									</span>
									{society.admission_open && (
										<span className="px-3 py-1 bg-green-100 text-green-700 rounded-full">
											Accepting Applications
										</span>
									)}
								</div>
							)}
						</div>
					</>
				) : (
					<div className="card text-center text-gray-500 py-12">
						No society assigned to you yet
					</div>
				)}
			</div>
		</DashboardLayout>
	);
};

export default SHDashboard;
