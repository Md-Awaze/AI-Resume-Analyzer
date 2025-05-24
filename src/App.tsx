import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Loader2, Upload, FileText } from "lucide-react";
import clsx from "clsx";
import AnalysisResults from "./components/AnalysisResults";

// Form validation schema
const formSchema = z.object({
	resume: z
		.instanceof(File)
		.refine(
			(file: File) => file.size <= 5 * 1024 * 1024,
			"File size must be less than 5MB"
		)
		.refine(
			(file: File) =>
				[
					"application/pdf",
					"application/msword",
					"application/vnd.openxmlformats-officedocument.wordprocessingml.document",
				].includes(file.type),
			"File must be PDF, DOC, or DOCX"
		),
	jobDescription: z
		.string()
		.min(1, "Job description is required")
		.max(2000, "Job description must be less than 2000 characters"),
});

type FormData = z.infer<typeof formSchema>;

function App() {
	const [isAnalyzing, setIsAnalyzing] = useState(false);
	const [progress, setProgress] = useState(0);
	const [showNotification, setShowNotification] = useState(false);
	const [dragActive, setDragActive] = useState(false);
	const [selectedFile, setSelectedFile] = useState<File | null>(null);
	const [analysisResults, setAnalysisResults] = useState<{
		skills: string[];
		suggestions: string[];
		matchScore: number;
		status: string;
	} | null>(null);

	const {
		register,
		handleSubmit,
		setValue,
		formState: { errors },
	} = useForm<FormData>({
		resolver: zodResolver(formSchema),
	});

	const onDrag = (e: React.DragEvent) => {
		e.preventDefault();
		e.stopPropagation();
		if (e.type === "dragenter" || e.type === "dragover") {
			setDragActive(true);
		} else if (e.type === "dragleave") {
			setDragActive(false);
		}
	};

	const onDrop = (e: React.DragEvent) => {
		e.preventDefault();
		e.stopPropagation();
		setDragActive(false);

		const file = e.dataTransfer?.files?.[0];
		if (file) {
			setSelectedFile(file);
			setValue("resume", file);
		}
	};

	const onFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
		const file = e.target?.files?.[0];
		if (file) {
			setSelectedFile(file);
		}
	};

	const onSubmit = async (data: FormData) => {
		try {
			setIsAnalyzing(true);
			setProgress(0);
			setAnalysisResults(null);

			// Show upload progress
			const interval = setInterval(() => {
				setProgress((prev) => {
					if (prev < 90) return prev + 10;
					return prev;
				});
			}, 500);

			// Create form data for the API call
			const formData = new FormData();
			formData.append("file", data.resume);
			formData.append("jobDescription", data.jobDescription);

			// Make the actual API call to upload the resume
			const response = await fetch(
				"http://127.0.0.1:5000/upload_resume",
				{
					method: "POST",
					body: formData,
				}
			);

			if (!response.ok) {
				throw new Error("Failed to upload resume");
			}

			const result = await response.json();

			clearInterval(interval);
			setProgress(100);

			// Set the analysis results
			setAnalysisResults({
				skills: ["JavaScript", "Python", "React", "Node.js", "SQL"], // TODO: Replace with actual skills from API
				suggestions: [
					"Add more details about your project achievements",
					"Include relevant certifications",
					"Highlight leadership experience",
				], // TODO: Replace with actual suggestions from API
				matchScore: 85, // TODO: Replace with actual match score from API
				status:
					result.status === "success"
						? "Analysis completed successfully"
						: "Failed to analyze resume",
			});
			setShowNotification(true);
		} catch (error) {
			console.error("Error uploading resume:", error);
			setAnalysisResults({
				skills: [],
				suggestions: [],
				matchScore: 0,
				status:
					error instanceof Error
						? error.message
						: "Failed to analyze resume",
			});
			setShowNotification(true);
		} finally {
			setIsAnalyzing(false);
		}
	};

	return (
		<div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
			<div className="max-w-4xl mx-auto p-6 pt-16">
				<header className="text-center mb-12">
					<h1 className="text-3xl font-bold text-gray-900 mb-2">
						AI Resume Analyzer
					</h1>
					<p className="text-gray-600">
						Upload your resume and job description for AI-powered
						analysis and feedback
					</p>
				</header>

				<form
					onSubmit={handleSubmit(onSubmit)}
					className="space-y-8 bg-white rounded-xl shadow-sm p-8 mb-8"
				>
					{/* Resume Upload Section */}
					<div className="space-y-4">
						<label className="block text-lg font-semibold text-gray-900">
							Resume Upload
						</label>
						<div
							className={clsx(
								"border-2 border-dashed rounded-lg p-8 text-center transition-colors",
								dragActive
									? "border-blue-500 bg-blue-50"
									: "border-gray-300 hover:border-blue-500",
								errors.resume ? "border-red-500" : ""
							)}
							onDragEnter={onDrag}
							onDragLeave={onDrag}
							onDragOver={onDrag}
							onDrop={onDrop}
						>
							<input
								type="file"
								{...register("resume", {
									onChange: onFileSelect,
								})}
								className="hidden"
								id="resume"
								accept=".pdf,.doc,.docx"
							/>
							<label
								htmlFor="resume"
								className="cursor-pointer block"
							>
								{selectedFile ? (
									<div className="flex flex-col items-center">
										<FileText className="mx-auto h-12 w-12 text-blue-500" />
										<p className="mt-2 text-sm text-gray-600">
											{selectedFile.name}
										</p>
										<p className="text-xs text-gray-500">
											Click to change file
										</p>
									</div>
								) : (
									<div className="flex flex-col items-center">
										<Upload className="mx-auto h-12 w-12 text-gray-400" />
										<p className="mt-2 text-sm text-gray-600">
											Click to upload or drag and drop
										</p>
										<p className="text-xs text-gray-500">
											PDF, DOC, or DOCX (max 5MB)
										</p>
									</div>
								)}
							</label>
						</div>
						{errors.resume && (
							<p className="text-sm text-red-500">
								{errors.resume.message}
							</p>
						)}
					</div>

					{/* Job Description Section */}
					<div className="space-y-4">
						<label className="block text-lg font-semibold text-gray-900">
							Job Description
						</label>
						<textarea
							{...register("jobDescription")}
							className={clsx(
								"w-full h-32 p-3 border rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none",
								errors.jobDescription
									? "border-red-500"
									: "border-gray-300"
							)}
							placeholder="Paste the job description here..."
						/>
						{errors.jobDescription && (
							<p className="text-sm text-red-500">
								{errors.jobDescription.message}
							</p>
						)}
					</div>

					{/* Progress Bar */}
					{isAnalyzing && (
						<div className="space-y-2">
							<div className="h-2 bg-gray-200 rounded-full overflow-hidden">
								<div
									className="h-full bg-blue-500 transition-all duration-500"
									style={{ width: `${progress}%` }}
								/>
							</div>
							<p className="text-sm text-gray-600 text-center">
								Analyzing your resume...
							</p>
						</div>
					)}

					{/* Submit Button */}
					<button
						type="submit"
						disabled={isAnalyzing}
						className={clsx(
							"w-full py-3 px-4 rounded-lg text-white font-medium transition-colors",
							isAnalyzing
								? "bg-gray-400 cursor-not-allowed"
								: "bg-blue-600 hover:bg-blue-700"
						)}
					>
						{isAnalyzing ? (
							<span className="flex items-center justify-center">
								<Loader2 className="animate-spin mr-2" />
								Analyzing...
							</span>
						) : (
							"Analyze Resume"
						)}
					</button>
				</form>

				{/* Analysis Results */}
				<AnalysisResults
					results={analysisResults}
					showNotification={showNotification}
					onHideNotification={() => setShowNotification(false)}
				/>
			</div>
		</div>
	);
}

export default App;
