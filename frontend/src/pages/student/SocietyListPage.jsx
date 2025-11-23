import { useState, useEffect } from "react";
import DashboardLayout from "../../components/Layout/DashboardLayout";
import SocietyCard from "../../components/SocietyCard";
import axiosClient from "../../api/axiosClient";

const SocietyListPage = () => {
	const [societies, setSocieties] = useState([]);
	const [loading, setLoading] = useState(true);
	const [category, setCategory] = useState("");

	useEffect(() => {
		fetchSocieties();
	}, [category]);

	const fetchSocieties = async () => {
		try {
			const params = category ? `?category=${category}` : "";
			const response = await axiosClient.get(`/societies/browse${params}`);
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
					<h1 className="text-3xl font-bold text-gray-900 mb-4">
						All Societies
					</h1>
					<div className="flex space-x-2">
						<button
							onClick={() => setCategory("")}
							className={`px-4 py-2 rounded-lg ${
								!category ? "btn-primary" : "btn-secondary"
							}`}
						>
							All
						</button>
						<button
							onClick={() => setCategory("Technical")}
							className={`px-4 py-2 rounded-lg ${
								category === "Technical" ? "btn-primary" : "btn-secondary"
							}`}
						>
							Technical
						</button>
						<button
							onClick={() => setCategory("Cultural")}
							className={`px-4 py-2 rounded-lg ${
								category === "Cultural" ? "btn-primary" : "btn-secondary"
							}`}
						>
							Cultural
						</button>
						<button
							onClick={() => setCategory("Sports")}
							className={`px-4 py-2 rounded-lg ${
								category === "Sports" ? "btn-primary" : "btn-secondary"
							}`}
						>
							Sports
						</button>
					</div>
				</div>

				{loading ? (
					<div className="text-center py-12">
						<div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
					</div>
				) : (
					<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
						{societies.map((society) => (
							<SocietyCard key={society.society_id} society={society} />
						))}
					</div>
				)}
			</div>
		</DashboardLayout>
	);
};

export default SocietyListPage;
