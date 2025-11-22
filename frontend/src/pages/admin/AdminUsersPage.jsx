import { useState, useEffect } from "react";
import DashboardLayout from "../../components/Layout/DashboardLayout";
import axiosClient from "../../api/axiosClient";

const AdminUsersPage = () => {
	const [users, setUsers] = useState([]);
	const [loading, setLoading] = useState(true);
	const [filter, setFilter] = useState("");

	useEffect(() => {
		fetchUsers();
	}, [filter]);

	const fetchUsers = async () => {
		try {
			const params = filter ? `?role=${filter}` : "";
			const response = await axiosClient.get(`/admin/users${params}`);
			setUsers(response.data.users || []);
		} catch (error) {
			console.error("Error fetching users:", error);
		} finally {
			setLoading(false);
		}
	};

	return (
		<DashboardLayout>
			<div className="max-w-7xl">
				<div className="mb-8">
					<h1 className="text-3xl font-bold text-gray-900 mb-4">
						Manage Users
					</h1>
					<div className="flex space-x-2">
						<button
							onClick={() => setFilter("")}
							className={!filter ? "btn-primary" : "btn-secondary"}
						>
							All
						</button>
						<button
							onClick={() => setFilter("student")}
							className={filter === "student" ? "btn-primary" : "btn-secondary"}
						>
							Students
						</button>
						<button
							onClick={() => setFilter("societyHead")}
							className={
								filter === "societyHead" ? "btn-primary" : "btn-secondary"
							}
						>
							Society Heads
						</button>
						<button
							onClick={() => setFilter("admin")}
							className={filter === "admin" ? "btn-primary" : "btn-secondary"}
						>
							Admins
						</button>
					</div>
				</div>

				{loading ? (
					<div className="text-center py-12">
						<div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
					</div>
				) : users.length > 0 ? (
					<div className="card overflow-hidden p-0">
						<table className="w-full">
							<thead className="bg-gray-50 border-b">
								<tr>
									<th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
										Name
									</th>
									<th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
										Email
									</th>
									<th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
										Role
									</th>
									<th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
										Joined
									</th>
								</tr>
							</thead>
							<tbody className="divide-y">
								{users.map((user) => (
									<tr key={user.user_id}>
										<td className="px-6 py-4 font-medium">{user.user_name}</td>
										<td className="px-6 py-4 text-sm text-gray-600">
											{user.user_email}
										</td>
										<td className="px-6 py-4">
											<span className="px-3 py-1 rounded-full text-xs font-medium bg-primary-100 text-primary-700">
												{user.user_role}
											</span>
										</td>
										<td className="px-6 py-4 text-sm text-gray-600">
											{new Date(user.created_at).toLocaleDateString()}
										</td>
									</tr>
								))}
							</tbody>
						</table>
					</div>
				) : (
					<div className="card text-center text-gray-500 py-12">
						No users found
					</div>
				)}
			</div>
		</DashboardLayout>
	);
};

export default AdminUsersPage;
