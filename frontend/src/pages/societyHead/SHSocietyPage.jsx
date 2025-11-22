import { useState, useEffect } from "react";
import DashboardLayout from "../../components/Layout/DashboardLayout";
import axiosClient from "../../api/axiosClient";

const SHSocietyPage = () => {
	const [society, setSociety] = useState(null);
	const [loading, setLoading] = useState(true);
	const [editing, setEditing] = useState(false);
	const [creating, setCreating] = useState(false);
	const [formData, setFormData] = useState({
		society_name: "",
		tagline: "",
		description: "",
		category: "Technical",
		admission_open: true,
	});

	useEffect(() => {
		fetchSociety();
	}, []);

	const fetchSociety = async () => {
		try {
			const response = await axiosClient.get("/societies/my-society");
			setSociety(response.data.society);
			if (response.data.society) {
				setFormData(response.data.society);
			}
		} catch (error) {
			console.error("Error fetching society:", error);
		} finally {
			setLoading(false);
		}
	};

	const handleCreate = async (e) => {
		e.preventDefault();
		try {
			await axiosClient.post("/societies", formData);
			alert("Society created successfully");
			setCreating(false);
			fetchSociety();
		} catch (error) {
			alert(error.response?.data?.message || "Failed to create society");
		}
	};

	const handleUpdate = async (e) => {
		e.preventDefault();
		try {
			await axiosClient.put(`/societies/${society.society_id}`, formData);
			alert("Society updated successfully");
			setEditing(false);
			fetchSociety();
		} catch (error) {
			alert("Failed to update society");
		}
	};

	return (
		<DashboardLayout>
			<div className="max-w-4xl">
				<h1 className="text-3xl font-bold text-gray-900 mb-8">
					Manage My Society
				</h1>

				{loading ? (
					<div className="text-center py-12">
						<div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
					</div>
				) : society ? (
					<div className="card">
						{!editing ? (
							<>
								<div className="flex justify-between items-start mb-6">
									<div>
										<h2 className="text-2xl font-bold mb-2">
											{society.society_name}
										</h2>
										<p className="text-gray-600">{society.tagline}</p>
									</div>
									<button
										onClick={() => {
											setFormData(society);
											setEditing(true);
										}}
										className="btn-primary"
									>
										Edit
									</button>
								</div>
								<div className="space-y-4">
									<div>
										<label className="block text-sm font-medium text-gray-700 mb-1">
											Description
										</label>
										<p className="text-gray-600">{society.description}</p>
									</div>
									<div>
										<label className="block text-sm font-medium text-gray-700 mb-1">
											Category
										</label>
										<p className="text-gray-600">{society.category}</p>
									</div>
									<div>
										<label className="block text-sm font-medium text-gray-700 mb-1">
											Members
										</label>
										<p className="text-gray-600">{society.member_count}</p>
									</div>
									<div>
										<label className="block text-sm font-medium text-gray-700 mb-1">
											Admission Status
										</label>
										<p className="text-gray-600">
											{society.admission_open ? "Open" : "Closed"}
										</p>
									</div>
								</div>
							</>
						) : (
							<form onSubmit={handleUpdate} className="space-y-4">
								<div>
									<label className="block text-sm font-medium text-gray-700 mb-2">
										Tagline
									</label>
									<input
										type="text"
										value={formData.tagline || ""}
										onChange={(e) =>
											setFormData({ ...formData, tagline: e.target.value })
										}
										className="input-field"
									/>
								</div>
								<div>
									<label className="block text-sm font-medium text-gray-700 mb-2">
										Description
									</label>
									<textarea
										value={formData.description || ""}
										onChange={(e) =>
											setFormData({ ...formData, description: e.target.value })
										}
										className="input-field"
										rows={4}
									/>
								</div>
								<div>
									<label className="block text-sm font-medium text-gray-700 mb-2">
										<input
											type="checkbox"
											checked={formData.admission_open || false}
											onChange={(e) =>
												setFormData({
													...formData,
													admission_open: e.target.checked,
												})
											}
											className="mr-2"
										/>
										Admission Open
									</label>
								</div>
								<div className="flex space-x-3">
									<button type="submit" className="btn-primary">
										Save Changes
									</button>
									<button
										type="button"
										onClick={() => setEditing(false)}
										className="btn-secondary"
									>
										Cancel
									</button>
								</div>
							</form>
						)}
					</div>
				) : (
					<div className="card">
						{!creating ? (
							<div className="text-center py-12">
								<h3 className="text-xl font-semibold text-gray-700 mb-4">
									No Society Assigned
								</h3>
								<p className="text-gray-600 mb-6">
									You don't have a society yet. Create one to get started!
								</p>
								<button
									onClick={() => setCreating(true)}
									className="btn-primary"
								>
									Create My Society
								</button>
							</div>
						) : (
							<form onSubmit={handleCreate} className="space-y-4">
								<h3 className="text-xl font-semibold mb-4">
									Create New Society
								</h3>

								<div>
									<label className="block text-sm font-medium text-gray-700 mb-2">
										Society Name *
									</label>
									<input
										type="text"
										required
										value={formData.society_name}
										onChange={(e) =>
											setFormData({ ...formData, society_name: e.target.value })
										}
										className="input-field"
										placeholder="e.g., Table Tennis Club"
									/>
								</div>

								<div>
									<label className="block text-sm font-medium text-gray-700 mb-2">
										Tagline
									</label>
									<input
										type="text"
										value={formData.tagline}
										onChange={(e) =>
											setFormData({ ...formData, tagline: e.target.value })
										}
										className="input-field"
										placeholder="A short catchy phrase about your society"
									/>
								</div>

								<div>
									<label className="block text-sm font-medium text-gray-700 mb-2">
										Description *
									</label>
									<textarea
										required
										value={formData.description}
										onChange={(e) =>
											setFormData({ ...formData, description: e.target.value })
										}
										className="input-field"
										rows={4}
										placeholder="Describe your society's mission and activities"
									/>
								</div>

								<div>
									<label className="block text-sm font-medium text-gray-700 mb-2">
										Category *
									</label>
									<select
										value={formData.category}
										onChange={(e) =>
											setFormData({ ...formData, category: e.target.value })
										}
										className="input-field"
									>
										<option value="Technical">Technical</option>
										<option value="Cultural">Cultural</option>
										<option value="Sports">Sports</option>
										<option value="Literary">Literary</option>
										<option value="Social">Social</option>
									</select>
								</div>

								<div>
									<label className="flex items-center text-sm font-medium text-gray-700">
										<input
											type="checkbox"
											checked={formData.admission_open}
											onChange={(e) =>
												setFormData({
													...formData,
													admission_open: e.target.checked,
												})
											}
											className="mr-2"
										/>
										Open for admissions
									</label>
								</div>

								<div className="flex space-x-3 pt-4">
									<button type="submit" className="btn-primary">
										Create Society
									</button>
									<button
										type="button"
										onClick={() => setCreating(false)}
										className="btn-secondary"
									>
										Cancel
									</button>
								</div>
							</form>
						)}
					</div>
				)}
			</div>
		</DashboardLayout>
	);
};

export default SHSocietyPage;
