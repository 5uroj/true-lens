import React, { useEffect } from 'react';
import {
  CheckCircle2,
  AlertCircle,
  AlertTriangle,
  Info,
  X
} from 'lucide-react';

const Alert = ({
  variant = 'info',
  title,
  message,
  onClose,
  duration = 3000
}) => {

  useEffect(() => {
    if (!onClose) return;
    const timer = setTimeout(onClose, duration);
    return () => clearTimeout(timer);
  }, [onClose, duration]);

  const variants = {
    success: {
      bg: 'bg-emerald-50',
      border: 'border-emerald-200',
      text: 'text-emerald-800',
      icon: <CheckCircle2 className="w-5 h-5 text-emerald-500" />
    },
    error: {
      bg: 'bg-rose-50',
      border: 'border-rose-200',
      text: 'text-rose-800',
      icon: <AlertCircle className="w-5 h-5 text-rose-500" />
    },
    warning: {
      bg: 'bg-amber-50',
      border: 'border-amber-200',
      text: 'text-amber-800',
      icon: <AlertTriangle className="w-5 h-5 text-amber-500" />
    },
    info: {
      bg: 'bg-indigo-50',
      border: 'border-indigo-200',
      text: 'text-indigo-800',
      icon: <Info className="w-5 h-5 text-indigo-500" />
    }
  };

  const style = variants[variant] || variants.info;

  return (
    <div className="fixed top-4 right-4 z-50 animate-slide-in">
      <div className={`flex items-start gap-3 p-4 rounded-xl border margin-top-15 shadow-lg w-80 ${style.bg} ${style.border} z-50`}>
        {style.icon}

        <div className="flex-1">
          <h4 className={`text-sm font-semibold ${style.text}`}>
            {title}
          </h4>
          <p className={`text-xs mt-1 ${style.text} opacity-80`}>
            {message}
          </p>
        </div>

        <button
          onClick={onClose}
          className="p-2 rounded-lg hover:bg-black/5"
          aria-label="Close"
        >
          <X className="w-4 h-4 text-gray-500" />
        </button>
      </div>
    </div>
  );
};

export default Alert;
