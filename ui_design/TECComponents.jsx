// TEC: BITLYFE IS THE NEW SHIT - Interface Design System
// The Creator's Rebellion - React Component Library

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronRightIcon, CpuChipIcon, SparklesIcon } from '@heroicons/react/24/outline';

// Core Design Tokens
export const TECDesignSystem = {
  colors: {
    primary: {
      purple: '#6366f1',
      violet: '#8b5cf6',
      blue: '#3b82f6',
      cyan: '#06b6d4',
    },
    accent: {
      green: '#10b981',
      yellow: '#f59e0b',
      red: '#ef4444',
      pink: '#ec4899',
    },
    neutral: {
      900: '#111827',
      800: '#1f2937',
      700: '#374151',
      600: '#4b5563',
      500: '#6b7280',
      400: '#9ca3af',
      300: '#d1d5db',
      200: '#e5e7eb',
      100: '#f3f4f6',
    },
    glow: {
      purple: 'rgba(139, 92, 246, 0.3)',
      blue: 'rgba(59, 130, 246, 0.3)',
      green: 'rgba(16, 185, 129, 0.3)',
    }
  },
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
    xxl: '3rem',
  },
  typography: {
    fontFamily: "'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif",
    fontSizes: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      xxl: '1.5rem',
      xxxl: '2rem',
    }
  },
  effects: {
    glassmorphism: {
      background: 'rgba(255, 255, 255, 0.1)',
      backdropFilter: 'blur(10px)',
      border: '1px solid rgba(255, 255, 255, 0.2)',
    },
    neonGlow: {
      boxShadow: '0 0 20px rgba(139, 92, 246, 0.5)',
      filter: 'drop-shadow(0 0 10px rgba(139, 92, 246, 0.7))',
    }
  }
};

// Base Button Component
export const TECButton = ({ 
  variant = 'primary', 
  size = 'md', 
  disabled = false, 
  loading = false, 
  icon, 
  children, 
  onClick,
  className = '',
  ...props 
}) => {
  const variants = {
    primary: 'bg-gradient-to-r from-purple-600 to-violet-600 hover:from-purple-700 hover:to-violet-700 text-white',
    secondary: 'bg-gray-800 hover:bg-gray-700 text-white border border-gray-600',
    danger: 'bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700 text-white',
    ghost: 'bg-transparent hover:bg-gray-800 text-gray-300 border border-gray-600',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <motion.button
      whileHover={{ scale: 1.02, y: -2 }}
      whileTap={{ scale: 0.98 }}
      className={`
        ${variants[variant]} 
        ${sizes[size]} 
        rounded-lg font-semibold transition-all duration-200
        shadow-lg hover:shadow-xl
        ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
        ${loading ? 'cursor-wait' : ''}
        ${className}
      `}
      disabled={disabled || loading}
      onClick={onClick}
      {...props}
    >
      <div className="flex items-center justify-center space-x-2">
        {loading && (
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
            className="w-4 h-4 border-2 border-current border-t-transparent rounded-full"
          />
        )}
        {icon && !loading && <span className="w-4 h-4">{icon}</span>}
        <span>{children}</span>
      </div>
    </motion.button>
  );
};

// Daisy Purecode Avatar Component
export const DaisyAvatar = ({ 
  state = 'idle', 
  size = 'md', 
  showPulse = true,
  className = '' 
}) => {
  const [isBreathing, setIsBreathing] = useState(true);
  
  const sizes = {
    sm: 'w-8 h-8',
    md: 'w-12 h-12',
    lg: 'w-16 h-16',
    xl: 'w-24 h-24',
  };

  const stateColors = {
    idle: 'from-purple-500 to-violet-500',
    thinking: 'from-blue-500 to-cyan-500',
    responding: 'from-green-500 to-emerald-500',
    error: 'from-red-500 to-pink-500',
  };

  return (
    <div className={`relative ${sizes[size]} ${className}`}>
      {/* Main Avatar */}
      <motion.div
        animate={isBreathing ? { scale: [1, 1.1, 1] } : {}}
        transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
        className={`
          w-full h-full rounded-full
          bg-gradient-to-r ${stateColors[state]}
          shadow-lg relative overflow-hidden
        `}
      >
        {/* Inner glow */}
        <div className="absolute inset-2 bg-white/20 rounded-full" />
        
        {/* Center core */}
        <div className="absolute inset-4 bg-white/40 rounded-full" />
        
        {/* Thinking animation */}
        {state === 'thinking' && (
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className="absolute inset-1 border-2 border-white/30 border-t-white/70 rounded-full"
          />
        )}
        
        {/* Speaking animation */}
        {state === 'responding' && (
          <motion.div
            animate={{ scale: [1, 1.2, 1] }}
            transition={{ duration: 0.5, repeat: Infinity }}
            className="absolute inset-3 bg-white/30 rounded-full"
          />
        )}
      </motion.div>
      
      {/* Pulse effect */}
      {showPulse && (
        <motion.div
          animate={{ scale: [1, 1.5, 1], opacity: [0.5, 0, 0.5] }}
          transition={{ duration: 2, repeat: Infinity }}
          className={`
            absolute inset-0 rounded-full
            bg-gradient-to-r ${stateColors[state]}
            -z-10
          `}
        />
      )}
      
      {/* Status indicator */}
      <div className="absolute -bottom-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-gray-800" />
    </div>
  );
};

// Module Card Component
export const ModuleCard = ({ 
  title, 
  description, 
  icon, 
  status = 'active', 
  onClick,
  className = '',
  children 
}) => {
  const [isHovered, setIsHovered] = useState(false);
  
  const statusColors = {
    active: 'border-green-500 bg-green-500/10',
    inactive: 'border-gray-600 bg-gray-600/10',
    error: 'border-red-500 bg-red-500/10',
  };

  return (
    <motion.div
      whileHover={{ scale: 1.02, y: -4 }}
      whileTap={{ scale: 0.98 }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      className={`
        relative p-6 rounded-xl cursor-pointer
        bg-gray-800/50 backdrop-blur-sm border border-gray-700
        hover:border-purple-500/50 transition-all duration-300
        ${className}
      `}
      onClick={onClick}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-purple-600/20 rounded-lg">
            {icon}
          </div>
          <div>
            <h3 className="text-lg font-semibold text-white">{title}</h3>
            <p className="text-sm text-gray-400">{description}</p>
          </div>
        </div>
        
        {/* Status indicator */}
        <div className={`px-2 py-1 rounded-full text-xs font-medium ${statusColors[status]}`}>
          {status}
        </div>
      </div>
      
      {/* Content */}
      {children}
      
      {/* Hover arrow */}
      <AnimatePresence>
        {isHovered && (
          <motion.div
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -10 }}
            className="absolute top-4 right-4"
          >
            <ChevronRightIcon className="w-5 h-5 text-purple-400" />
          </motion.div>
        )}
      </AnimatePresence>
      
      {/* Background glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-purple-600/5 to-violet-600/5 rounded-xl opacity-0 hover:opacity-100 transition-opacity duration-300" />
    </motion.div>
  );
};

// Chat Message Component
export const ChatMessage = ({ 
  message, 
  isUser = false, 
  timestamp, 
  provider,
  avatar,
  className = '' 
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex items-start space-x-3 mb-4 ${className}`}
    >
      {/* Avatar */}
      {!isUser && (
        <div className="flex-shrink-0">
          {avatar || <DaisyAvatar size="sm" />}
        </div>
      )}
      
      {/* Message content */}
      <div className={`flex-1 ${isUser ? 'text-right' : ''}`}>
        {/* Message bubble */}
        <div className={`
          inline-block max-w-xs lg:max-w-md px-4 py-2 rounded-lg
          ${isUser 
            ? 'bg-purple-600 text-white ml-auto' 
            : 'bg-gray-700 text-gray-100'
          }
        `}>
          <p className="text-sm">{message}</p>
        </div>
        
        {/* Metadata */}
        <div className={`flex items-center space-x-2 mt-1 text-xs text-gray-500 ${isUser ? 'justify-end' : ''}`}>
          <span>{timestamp}</span>
          {provider && !isUser && (
            <span className="px-2 py-0.5 bg-gray-600 rounded-full">{provider}</span>
          )}
        </div>
      </div>
      
      {/* User avatar */}
      {isUser && (
        <div className="flex-shrink-0">
          <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
            <span className="text-white text-sm font-medium">U</span>
          </div>
        </div>
      )}
    </motion.div>
  );
};

// Progress Bar Component
export const ProgressBar = ({ 
  value = 0, 
  max = 100, 
  label, 
  variant = 'default',
  showValue = true,
  className = '' 
}) => {
  const percentage = Math.min((value / max) * 100, 100);
  
  const variants = {
    default: 'from-purple-500 to-violet-500',
    health: 'from-green-500 to-emerald-500',
    xp: 'from-yellow-500 to-orange-500',
    mana: 'from-blue-500 to-cyan-500',
  };

  return (
    <div className={`${className}`}>
      {/* Label */}
      {label && (
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-300">{label}</span>
          {showValue && (
            <span className="text-sm text-gray-400">{value}/{max}</span>
          )}
        </div>
      )}
      
      {/* Progress bar */}
      <div className="w-full bg-gray-700 rounded-full h-2 overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 1, ease: "easeOut" }}
          className={`h-full bg-gradient-to-r ${variants[variant]} rounded-full relative`}
        >
          {/* Glow effect */}
          <div className="absolute inset-0 bg-white/20 rounded-full" />
        </motion.div>
      </div>
    </div>
  );
};

// Input Field Component
export const TECInput = ({
  label,
  type = 'text',
  placeholder,
  value,
  onChange,
  error,
  icon,
  className = '',
  ...props
}) => {
  const [isFocused, setIsFocused] = useState(false);
  
  return (
    <div className={`${className}`}>
      {/* Label */}
      {label && (
        <label className="block text-sm font-medium text-gray-300 mb-2">
          {label}
        </label>
      )}
      
      {/* Input wrapper */}
      <div className="relative">
        {/* Icon */}
        {icon && (
          <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
            {icon}
          </div>
        )}
        
        {/* Input */}
        <input
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          className={`
            w-full px-4 py-2 bg-gray-800 border border-gray-600 rounded-lg
            text-white placeholder-gray-400
            focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent
            transition-all duration-200
            ${icon ? 'pl-10' : ''}
            ${error ? 'border-red-500' : ''}
          `}
          {...props}
        />
        
        {/* Focus glow */}
        {isFocused && (
          <div className="absolute inset-0 bg-purple-500/20 rounded-lg pointer-events-none" />
        )}
      </div>
      
      {/* Error message */}
      {error && (
        <p className="mt-1 text-sm text-red-400">{error}</p>
      )}
    </div>
  );
};

// Loading Spinner Component
export const LoadingSpinner = ({ 
  size = 'md', 
  color = 'purple',
  className = '' 
}) => {
  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
    xl: 'w-12 h-12',
  };
  
  const colors = {
    purple: 'border-purple-500',
    blue: 'border-blue-500',
    green: 'border-green-500',
    white: 'border-white',
  };

  return (
    <motion.div
      animate={{ rotate: 360 }}
      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
      className={`
        ${sizes[size]} border-2 ${colors[color]} border-t-transparent rounded-full
        ${className}
      `}
    />
  );
};

// Notification Component
export const Notification = ({ 
  type = 'info', 
  title, 
  message, 
  onClose,
  className = '' 
}) => {
  const types = {
    info: 'bg-blue-500/20 border-blue-500 text-blue-100',
    success: 'bg-green-500/20 border-green-500 text-green-100',
    warning: 'bg-yellow-500/20 border-yellow-500 text-yellow-100',
    error: 'bg-red-500/20 border-red-500 text-red-100',
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -50, scale: 0.9 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -50, scale: 0.9 }}
      className={`
        p-4 rounded-lg border backdrop-blur-sm
        ${types[type]} ${className}
      `}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          {title && (
            <h4 className="font-semibold mb-1">{title}</h4>
          )}
          <p className="text-sm opacity-90">{message}</p>
        </div>
        
        {onClose && (
          <button
            onClick={onClose}
            className="ml-4 text-current hover:opacity-70 transition-opacity"
          >
            <XMarkIcon className="w-5 h-5" />
          </button>
        )}
      </div>
    </motion.div>
  );
};

// Modal Component
export const Modal = ({ 
  isOpen, 
  onClose, 
  title, 
  children,
  className = '' 
}) => {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            onClick={onClose}
          />
          
          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            className={`
              fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2
              bg-gray-800 rounded-xl border border-gray-700 shadow-2xl
              max-w-md w-full max-h-[90vh] overflow-auto z-50
              ${className}
            `}
          >
            {/* Header */}
            {title && (
              <div className="flex items-center justify-between p-6 border-b border-gray-700">
                <h2 className="text-xl font-semibold text-white">{title}</h2>
                <button
                  onClick={onClose}
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  <XMarkIcon className="w-6 h-6" />
                </button>
              </div>
            )}
            
            {/* Content */}
            <div className="p-6">
              {children}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

// Export all components
export {
  TECDesignSystem,
  TECButton,
  DaisyAvatar,
  ModuleCard,
  ChatMessage,
  ProgressBar,
  TECInput,
  LoadingSpinner,
  Notification,
  Modal,
};
