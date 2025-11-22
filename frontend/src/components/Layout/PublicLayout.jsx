import Navbar from "../Navbar";

const PublicLayout = ({ children }) => {
	return (
		<div className="min-h-screen bg-gray-50">
			<Navbar />
			<main>{children}</main>
		</div>
	);
};

export default PublicLayout;
