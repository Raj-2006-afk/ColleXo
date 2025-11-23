import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import DashboardLayout from "../../components/Layout/DashboardLayout";
import axiosClient from "../../api/axiosClient";

const FormSubmissionPage = () => {
	const { formId } = useParams();
	const navigate = useNavigate();
	const [form, setForm] = useState(null);
	const [loading, setLoading] = useState(true);
	const [submitting, setSubmitting] = useState(false);
	const [responses, setResponses] = useState({});
	const [error, setError] = useState("");

	useEffect(() => {
		fetchForm();
	}, [formId]);

	const fetchForm = async () => {
		try {
			const response = await axiosClient.get(`/forms/${formId}`);
			setForm(response.data);
			// Initialize responses object
			const initialResponses = {};
			response.data.questions?.forEach((q) => {
				initialResponses[q.question_id] = "";
			});
			setResponses(initialResponses);
		} catch (error) {
			console.error("Error fetching form:", error);
			setError("Failed to load form");
		} finally {
			setLoading(false);
		}
	};

	const handleInputChange = (questionId, value) => {
		setResponses({
			...responses,
			[questionId]: value,
		});
	};

	const handleSubmit = async (e) => {
		e.preventDefault();
		setError("");

		// Validate required fields
		const missingRequired = form.questions?.filter(
			(q) => q.is_required && !responses[q.question_id]?.trim()
		);

		if (missingRequired?.length > 0) {
			setError("Please fill all required fields");
			return;
		}

		setSubmitting(true);
		try {
			await axiosClient.post("/applications", {
				form_id: parseInt(formId),
				responses: responses,
			});

			alert("Application submitted successfully!");
			navigate("/student/societies");
		} catch (error) {
			console.error("Error submitting application:", error);
			setError(error.response?.data?.error || "Failed to submit application");
		} finally {
			setSubmitting(false);
		}
	};

	const renderQuestion = (question) => {
		const commonProps = {
			id: `question-${question.question_id}`,
			value: responses[question.question_id] || "",
			onChange: (e) => handleInputChange(question.question_id, e.target.value),
			required: question.is_required,
			className:
				"w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent",
		};

		switch (question.question_type) {
			case "textarea":
				return <textarea {...commonProps} rows="4" />;

			case "select":
				return (
					<select {...commonProps}>
						<option value="">Select an option</option>
						{question.options?.split(",").map((option, idx) => (
							<option key={idx} value={option.trim()}>
								{option.trim()}
							</option>
						))}
					</select>
				);

			case "email":
				return <input {...commonProps} type="email" />;

			case "tel":
				return <input {...commonProps} type="tel" />;

			case "number":
				return <input {...commonProps} type="number" />;

			case "text":
			default:
				return <input {...commonProps} type="text" />;
		}
	};

	if (loading) {
		return (
			<DashboardLayout>
				<div className="flex justify-center items-center min-h-screen">
					<div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
				</div>
			</DashboardLayout>
		);
	}

	if (!form) {
		return (
			<DashboardLayout>
				<div className="max-w-4xl mx-auto">
					<div className="bg-red-50 border border-red-200 rounded-lg p-4">
						<p className="text-red-600">Form not found</p>
					</div>
				</div>
			</DashboardLayout>
		);
	}

	return (
		<DashboardLayout>
			<div className="max-w-4xl mx-auto">
				<div className="bg-white rounded-lg shadow-md p-8">
					{/* Header */}
					<div className="mb-8">
						<div className="flex items-center mb-4">
							{form.logo_url && (
								<img
									src={form.logo_url}
									alt={form.society_name}
									className="w-16 h-16 object-cover rounded-lg mr-4"
								/>
							)}
							<div>
								<h1 className="text-3xl font-bold text-gray-900">
									{form.title}
								</h1>
								<p className="text-gray-600">
									{form.society_name} • {form.category}
								</p>
							</div>
						</div>
						<div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
							<p className="text-sm text-blue-800">
								<span className="font-semibold">Note:</span> Fields marked with
								* are required
							</p>
						</div>
					</div>

					{/* Error Message */}
					{error && (
						<div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
							<p className="text-red-600">{error}</p>
						</div>
					)}

					{/* Form */}
					<form onSubmit={handleSubmit} className="space-y-6">
						{form.questions?.map((question, index) => (
							<div key={question.question_id} className="space-y-2">
								<label
									htmlFor={`question-${question.question_id}`}
									className="block text-sm font-medium text-gray-700"
								>
									{index + 1}. {question.question_text}
									{question.is_required && (
										<span className="text-red-500 ml-1">*</span>
									)}
								</label>
								{renderQuestion(question)}
							</div>
						))}

						{/* Submit Button */}
						<div className="flex justify-between items-center pt-6 border-t">
							<button
								type="button"
								onClick={() => navigate("/student/societies")}
								className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
							>
								Cancel
							</button>
							<button
								type="submit"
								disabled={submitting}
								className="btn-primary px-8 py-3 disabled:opacity-50 disabled:cursor-not-allowed"
							>
								{submitting ? "Submitting..." : "Submit Application"}
							</button>
						</div>
					</form>
				</div>
			</div>
		</DashboardLayout>
	);
};

export default FormSubmissionPage;
