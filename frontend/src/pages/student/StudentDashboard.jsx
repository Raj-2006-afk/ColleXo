import { useState, useEffect } from "react";
import DashboardLayout from "../../components/Layout/DashboardLayout";
import SocietyCard from "../../components/SocietyCard";
import axiosClient from "../../api/axiosClient";

const StudentDashboard = () => {
	const [societies, setSocieties] = useState([]);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		fetchSocieties();
	}, []);

	const fetchSocieties = async () => {
		try {
			const response = await axiosClient.get(
				"/societies?per_page=6&admission_open=true"
			);
			setSocieties(response.data.societies || []);
		} catch (error) {
			console.error("Error fetching societies:", error);
		} finally {
			setLoading(false);
		}
	};

	return (
		<DashboardLayout>
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
			</div>
		</DashboardLayout>
	);
};

export default StudentDashboard;
