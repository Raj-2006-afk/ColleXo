import { useState, useEffect } from "react";
import DashboardLayout from "../../components/Layout/DashboardLayout";
import StatusPill from "../../components/StatusPill";
import axiosClient from "../../api/axiosClient";

const SHFormsPage = () => {
	const [forms, setForms] = useState([]);
	const [society, setSociety] = useState(null);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		fetchData();
	}, []);

	const fetchData = async () => {
		try {
			const societyRes = await axiosClient.get("/societies/my-society");
			setSociety(societyRes.data.society);

			if (societyRes.data.society) {
				const formsRes = await axiosClient.get(
					`/forms/society/${societyRes.data.society.society_id}`
				);
				setForms(formsRes.data.forms || []);
			}
		} catch (error) {
			console.error("Error fetching forms:", error);
		} finally {
			setLoading(false);
		}
	};

	const createForm = async () => {
		const title = prompt("Enter form title:");
		if (!title) return;

		try {
			await axiosClient.post("/forms", {
				society_id: society.society_id,
				title,
				status: "draft",
			});
			fetchData();
		} catch (error) {
			alert("Failed to create form");
		}
	};

	const toggleStatus = async (formId, currentStatus) => {
		const newStatus = currentStatus === "published" ? "draft" : "published";
		try {
			await axiosClient.put(`/forms/${formId}`, { status: newStatus });
			fetchData();
		} catch (error) {
			alert("Failed to update form");
		}
	};

	return (
		<DashboardLayout>
			<div className="max-w-7xl">
				<div className="flex justify-between items-center mb-8">
					<h1 className="text-3xl font-bold text-gray-900">
						Recruitment Forms
					</h1>
					<button onClick={createForm} className="btn-primary">
						Create New Form
					</button>
				</div>

				{loading ? (
					<div className="text-center py-12">
						<div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
					</div>
				) : forms.length > 0 ? (
					<div className="grid gap-4">
						{forms.map((form) => (
							<div
								key={form.form_id}
								className="card flex justify-between items-center"
							>
								<div>
									<h3 className="text-lg font-semibold">{form.title}</h3>
									<p className="text-sm text-gray-600">
										{form.application_count || 0} applications
									</p>
								</div>
								<div className="flex items-center space-x-3">
									<StatusPill status={form.status} />
									<button
										onClick={() => toggleStatus(form.form_id, form.status)}
										className="btn-secondary text-sm"
									>
										{form.status === "published" ? "Unpublish" : "Publish"}
									</button>
								</div>
							</div>
						))}
					</div>
				) : (
					<div className="card text-center text-gray-500 py-12">
						No forms created yet
					</div>
				)}
			</div>
		</DashboardLayout>
	);
};

export default SHFormsPage;
