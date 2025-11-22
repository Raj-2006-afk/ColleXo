import Navbar from "../Navbar";
import Sidebar from "../Sidebar";
import useAuth from "../../hooks/useAuth";

const DashboardLayout = ({ children }) => {
	const { user } = useAuth();

	return (
		<div className="min-h-screen bg-gray-50">
			<Navbar />
			<div className="flex">
				<Sidebar role={user?.user_role} />
				<main className="flex-1 p-8">{children}</main>
			</div>
		</div>
	);
};

export default DashboardLayout;
