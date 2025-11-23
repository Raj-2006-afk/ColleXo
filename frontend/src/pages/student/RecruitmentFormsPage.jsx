import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import DashboardLayout from "../../components/Layout/DashboardLayout";
import axiosClient from "../../api/axiosClient";

const RecruitmentFormsPage = () => {
	const [forms, setForms] = useState([]);
	const [myApplications, setMyApplications] = useState([]);
	const [loading, setLoading] = useState(true);
	const navigate = useNavigate();

	useEffect(() => {
		fetchData();
	}, []);

	const fetchData = async () => {
		try {
			const [formsRes, appsRes] = await Promise.all([
				axiosClient.get("/forms/published"),
				axiosClient.get("/applications/my-applications?per_page=100"),
			]);
			setForms(formsRes.data.forms || []);
			setMyApplications(appsRes.data.applications || []);
		} catch (error) {
			console.error("Error fetching data:", error);
		} finally {
			setLoading(false);
		}
	};

	const handleApply = (formId) => {
		navigate(`/student/form/${formId}`);
	};

	const isFormFilled = (formId) => {
		return myApplications.some((app) => app.form_id === formId);
	};

	return (
		<DashboardLayout>
			<div className="max-w-7xl">
				<div className="mb-8">
					<h1 className="text-3xl font-bold text-gray-900 mb-2">
						Recruitment Forms
					</h1>
					<p className="text-gray-600">
						Browse and apply to open recruitment forms from various societies
					</p>
				</div>

				{loading ? (
					<div className="text-center py-12">
						<div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
					</div>
				) : forms.length === 0 ? (
					<div className="text-center py-12 bg-white rounded-lg shadow">
						<p className="text-gray-600">
							No recruitment forms available at the moment
						</p>
					</div>
				) : (
					<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
						{forms.map((form) => (
							<div
								key={form.form_id}
								className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
							>
								<div className="flex items-start mb-4">
									{form.logo_url && (
										<img
											src={form.logo_url}
											alt={form.society_name}
											className="w-12 h-12 object-cover rounded-lg mr-3"
										/>
									)}
									<div className="flex-1">
										<h3 className="text-lg font-semibold text-gray-900 mb-1">
											{form.title}
										</h3>
										<p className="text-sm text-gray-600">{form.society_name}</p>
									</div>
								</div>

								<div className="flex items-center space-x-2 mb-4 text-xs">
									<span className="px-2 py-1 bg-primary-100 text-primary-700 rounded-full font-medium">
										{form.category}
									</span>
									<span className="text-gray-500">
										{form.application_count || 0} applications
									</span>
								</div>

								{isFormFilled(form.form_id) ? (
									<button
										disabled
										className="w-full py-2 text-sm bg-gray-300 text-gray-600 rounded-lg cursor-not-allowed font-medium"
									>
										✓ Filled
									</button>
								) : (
									<button
										onClick={() => handleApply(form.form_id)}
										className="w-full btn-primary py-2 text-sm"
									>
										Apply Now
									</button>
								)}
							</div>
						))}
					</div>
				)}
			</div>
		</DashboardLayout>
	);
};

export default RecruitmentFormsPage;
