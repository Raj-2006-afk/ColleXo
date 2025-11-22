import { useState, useEffect } from "react";
import DashboardLayout from "../../components/Layout/DashboardLayout";
import StatCard from "../../components/StatCard";
import axiosClient from "../../api/axiosClient";

const AdminDashboard = () => {
	const [stats, setStats] = useState(null);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		fetchStats();
	}, []);

	const fetchStats = async () => {
		try {
			const response = await axiosClient.get("/admin/dashboard/stats");
			setStats(response.data.stats);
		} catch (error) {
			console.error("Error fetching stats:", error);
		} finally {
			setLoading(false);
		}
	};

	return (
		<DashboardLayout>
			<div className="max-w-7xl">
				<h1 className="text-3xl font-bold text-gray-900 mb-8">
					Admin Dashboard
				</h1>

				{loading ? (
					<div className="text-center py-12">
						<div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
					</div>
				) : (
					<div className="grid md:grid-cols-4 gap-6">
						<StatCard
							title="Total Users"
							value={stats?.total_users || 0}
							icon="👥"
							color="primary"
						/>
						<StatCard
							title="Societies"
							value={stats?.total_societies || 0}
							icon="🏢"
							color="blue"
						/>
						<StatCard
							title="Forms"
							value={stats?.total_forms || 0}
							icon="📋"
							color="green"
						/>
						<StatCard
							title="Applications"
							value={stats?.total_applications || 0}
							icon="📬"
							color="yellow"
						/>
					</div>
				)}
			</div>
		</DashboardLayout>
	);
};

export default AdminDashboard;
