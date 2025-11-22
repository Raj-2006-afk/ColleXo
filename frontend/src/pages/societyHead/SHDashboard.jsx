import { useState, useEffect } from "react";
import DashboardLayout from "../../components/Layout/DashboardLayout";
import StatCard from "../../components/StatCard";
import axiosClient from "../../api/axiosClient";

const SHDashboard = () => {
	const [society, setSociety] = useState(null);
	const [stats, setStats] = useState(null);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		fetchData();
	}, []);

	const fetchData = async () => {
		try {
			const societyRes = await axiosClient.get("/societies/my-society");
			setSociety(societyRes.data.society);

			if (societyRes.data.society) {
				const appsRes = await axiosClient.get(
					`/applications/society/${societyRes.data.society.society_id}`
				);
				setStats(appsRes.data.statistics);
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
							<h2 className="text-xl font-semibold mb-4">
								{society.society_name}
							</h2>
							<p className="text-gray-600 mb-4">{society.description}</p>
							<div className="flex items-center space-x-4 text-sm text-gray-600">
								<span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full">
									{society.category}
								</span>
								<span>{society.member_count} members</span>
								{society.admission_open && (
									<span className="px-3 py-1 bg-green-100 text-green-700 rounded-full">
										Accepting Applications
									</span>
								)}
							</div>
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
