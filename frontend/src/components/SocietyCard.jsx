const SocietyCard = ({ society, onClick }) => {
	return (
		<div onClick={onClick} className="card-hover">
			<div className="flex items-start space-x-4">
				<div className="w-16 h-16 bg-gradient-to-br from-primary-400 to-primary-600 rounded-lg flex-shrink-0 flex items-center justify-center">
					{society.logo_url ? (
						<img
							src={society.logo_url}
							alt={society.society_name}
							className="w-full h-full rounded-lg object-cover"
						/>
					) : (
						<span className="text-white text-2xl font-bold">
							{society.society_name.charAt(0)}
						</span>
					)}
				</div>
				<div className="flex-1">
					<h3 className="text-lg font-semibold text-gray-900 mb-1">
						{society.society_name}
					</h3>
					<p className="text-sm text-gray-600 mb-2">{society.tagline}</p>
					<div className="flex items-center space-x-3 text-xs">
						<span className="px-2 py-1 bg-primary-100 text-primary-700 rounded-full font-medium">
							{society.category}
						</span>
						<span className="text-gray-500">
							{society.member_count} members
						</span>
						{society.admission_open && (
							<span className="px-2 py-1 bg-green-100 text-green-700 rounded-full font-medium">
								Open for Applications
							</span>
						)}
					</div>
				</div>
			</div>
		</div>
	);
};

export default SocietyCard;
