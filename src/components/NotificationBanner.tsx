import { useEffect } from "react";
import { AlertCircle, CheckCircle2, XCircle } from "lucide-react";
import clsx from "clsx";

interface NotificationBannerProps {
	message: string;
	type: "success" | "error" | "warning";
	show: boolean;
	onHide: () => void;
	duration?: number;
}

const ICONS = {
	success: CheckCircle2,
	error: XCircle,
	warning: AlertCircle,
};

const NotificationBanner: React.FC<NotificationBannerProps> = ({
	message,
	type,
	show,
	onHide,
	duration = 5000,
}) => {
	useEffect(() => {
		if (show) {
			const timer = setTimeout(() => {
				onHide();
			}, duration);
			return () => clearTimeout(timer);
		}
	}, [show, duration, onHide]);

	if (!show) return null;

	const Icon = ICONS[type];

	return (
		<div
			className={clsx(
				"fixed top-5 left-1/2 transform -translate-x-1/2",
				"flex items-center gap-2 px-6 py-4 rounded-lg shadow-lg z-50",
				"transition-opacity duration-300",
				type === "success" &&
					"bg-green-100 border-l-4 border-green-500 text-green-700",
				type === "error" &&
					"bg-red-100 border-l-4 border-red-500 text-red-700",
				type === "warning" &&
					"bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700"
			)}
			role="alert"
			aria-live="polite"
		>
			<Icon className="h-5 w-5" />
			<span>{message}</span>
		</div>
	);
};

export default NotificationBanner;
