def get_app_styles():
    return """
        /* Global Styles */
        QWidget {
            background-color: #111827;
            color: #F9FAFB;
            font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
        }
        
        /* Header - Fixed at top */
        #header {
            background-color: #1F2937;
            border-bottom: 1px solid #374151;
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        
        #logo-icon {
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                        stop:0 #4F46E5, stop:1 #10B981);
            border-radius: 8px;
            font-weight: bold;
            font-size: 18px;
        }
        
        #logo-text {
            font-size: 22px;
            font-weight: 700;
            color: #F9FAFB;
        }
        
        #nav-item-active {
            padding: 5px 20px;
            border-radius: 8px;
            background-color: #4F46E5;
            color: white;
            font-weight: 500;
            font-size: 15px;
            border: none;
        }
        
        #nav-item-active:hover {
            background-color: #4338CA;
        }
        
        #user-profile {
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
        }
        
        #user-profile:hover {
            background-color: rgba(255, 255, 255, 0.08);
        }
        
        #user-avatar {
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                        stop:0 #4F46E5, stop:1 #10B981);
            border-radius: 16px;
            font-weight: 600;
            font-size: 14px;
            color: white;
        }
        
        #user-name {
            font-size: 14px;
            font-weight: 600;
        }
        
        #user-role {
            font-size: 12px;
            color: #9CA3AF;
        }
        
        /* Page Header */
        #page-title {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        #page-subtitle {
            color: #9CA3AF;
            font-size: 15px;
        }
        
        /* Status Bar */
        #status-bar {
            background-color: #1F2937;
            border-radius: 12px;
            border: 1px solid #374151;
        }
        
        #status-label {
            font-size: 14px;
            color: #9CA3AF;
        }
        
        #status-value-ready {
            font-size: 16px;
            font-weight: 600;
            color: #10B981;
        }
        
        #status-value-uploaded {
            font-size: 16px;
            font-weight: 600;
            color: #F59E0B;
        }
        
        #status-value-processing {
            font-size: 16px;
            font-weight: 600;
            color: #4F46E5;
        }
        
        #status-value-complete {
            font-size: 16px;
            font-weight: 600;
            color: #10B981;
        }
        
        /* Info Cards */
        #info-card {
            background-color: #1F2937;
            border-radius: 12px;
            border: 1px solid #374151;
        }
        
        #info-card:hover {
            border-color: #4F46E5;
            transform: translateY(-2px);
        }
        
        #card-icon-blue {
            background-color: rgba(79, 70, 229, 0.2);
            color: #4F46E5;
            border-radius: 8px;
            font-size: 18px;
        }
        
        #card-icon-green {
            background-color: rgba(16, 185, 129, 0.2);
            color: #10B981;
            border-radius: 8px;
            font-size: 18px;
        }
        
        #card-icon-purple {
            background-color: rgba(168, 85, 247, 0.2);
            color: #A855F7;
            border-radius: 8px;
            font-size: 18px;
        }
        
        #card-icon-orange {
            background-color: rgba(245, 158, 11, 0.2);
            color: #F59E0B;
            border-radius: 8px;
            font-size: 18px;
        }
        
        #card-icon-red {
            background-color: rgba(239, 68, 68, 0.2);
            color: #EF4444;
            border-radius: 8px;
            font-size: 18px;
        }
        
        #card-label {
            color: #9CA3AF;
            font-size: 13px;
        }
        
        #card-value {
            font-size: 18px;
            font-weight: 600;
        }
        
        /* Processing Cards */
        #processing-card {
            background-color: #1F2937;
            border-radius: 12px;
            border: 1px solid #374151;
        }
        
        #card-header {
            border-bottom: 1px solid #374151;
        }
        
        #card-title {
            font-size: 18px;
            font-weight: 600;
        }
        
        #upload-btn {
            background-color: #4F46E5;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            font-size: 14px;
        }
        
        #upload-btn:hover {
            background-color: #4338CA;
        }
        
        /* Save Button */
        #save-btn {
            background-color: #10B981;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 600;
            font-size: 13px;
        }
        
        #save-btn:hover:enabled {
            background-color: #0DA271;
            transform: translateY(-2px);
        }
        
        #save-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        #status-badge-pending {
            background-color: rgba(245, 158, 11, 0.2);
            color: #F59E0B;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        
        #status-badge-processing {
            background-color: rgba(79, 70, 229, 0.2);
            color: #4F46E5;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        
        #status-badge-ready {
            background-color: rgba(16, 185, 129, 0.2);
            color: #10B981;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        
        #image-display-area {
            background-color: rgba(255, 255, 255, 0.03);
        }
        
        #image-placeholder {
            background-color: rgba(255, 255, 255, 0.03);
            border-radius: 8px;
            border: 2px dashed #374151;
        }
        
        #placeholder-icon {
            font-size: 64px;
            color: #9CA3AF;
            opacity: 0.7;
        }
        
        #placeholder-text {
            color: #9CA3AF;
            font-size: 16px;
            margin-bottom: 8px;
        }
        
        #placeholder-subtext {
            color: #9CA3AF;
            font-size: 14px;
            opacity: 0.7;
        }
        
        /* Control Panel */
        #control-panel {
            background-color: #1F2937;
            border-radius: 12px;
            border: 1px solid #374151;
        }
        
        #panel-title {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        #panel-subtitle {
            color: #9CA3AF;
            font-size: 14px;
            margin-bottom: 16px;
        }
        
        /* Process Section */
        #process-section {
            background-color: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            border: 1px dashed #374151;
            min-height: 320px;
            max-height: 350px;
        }
        
        #centered-container {
            min-height: 280px;
        }
        
        /* Filter Options */
        #filter-option {
            min-height: 200px;
        }
        
        #filter-label {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid #374151;
            border-radius: 12px;
            min-height: 180px;
        }
        
        QRadioButton:checked + #filter-label {
            border-color: #4F46E5;
            background-color: rgba(79, 70, 229, 0.1);
            box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
        }
        
        #filter-label:hover {
            background-color: rgba(255, 255, 255, 0.08);
            transform: translateY(-3px);
        }
        
        #filter-icon {
            background-color: rgba(79, 70, 229, 0.15);
            border-radius: 12px;
            color: #4F46E5;
            font-size: 20px;
            min-width: 44px;
            min-height: 44px;
        }
        
        #filter-name {
            font-weight: 600;
            font-size: 18px;
            color: #F9FAFB;
            margin-bottom: 2px;
        }
        
        #filter-description {
            font-size: 13px;
            color: #9CA3AF;
            line-height: 1.4;
            min-height: 60px;
            padding-top: 8px;
        }
        
        /* Threshold Widget */
        #threshold-widget {
            background-color: rgba(255, 255, 255, 0.03);
            border-radius: 8px;
            padding: 12px;
            margin-top: 8px;
        }
        
        #threshold-label {
            color: #9CA3AF;
            font-size: 13px;
            font-weight: 600;
        }
        
        #threshold-value-label {
            color: #4F46E5;
            font-size: 16px;
            font-weight: 700;
        }
        
        #threshold-slider {
            height: 20px;
            margin: 8px 0;
        }
        
        #threshold-slider::groove:horizontal {
            border: 1px solid #374151;
            height: 6px;
            background: #1F2937;
            border-radius: 3px;
        }
        
        #threshold-slider::handle:horizontal {
            background: #4F46E5;
            border: 1px solid #4338CA;
            width: 16px;
            height: 16px;
            border-radius: 8px;
            margin: -5px 0;
        }
        
        #threshold-slider::handle:horizontal:hover {
            background: #4338CA;
        }
        
        #threshold-explanation {
            color: #9CA3AF;
            font-size: 11px;
            margin-top: 8px;
            padding-top: 4px;
        }
        
        /* Process Button */
        #process-btn {
            padding: 16px 28px;
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                        stop:0 #4F46E5, stop:1 #4338CA);
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            font-size: 16px;
            min-width: 220px;
            min-height: 65px;
        }
        
        #process-btn:hover:enabled {
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                        stop:0 #4338CA, stop:1 #4F46E5);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(79, 70, 229, 0.4);
        }
        
        #process-btn:disabled {
            opacity: 0.5;
        }
        
        #button-description {
            color: #9CA3AF;
            font-size: 13px;
            line-height: 1.5;
            padding: 8px 12px;
            text-align: center;
        }
        
        QRadioButton {
            margin-right: -100px;
        }
        
        /* Hide scrollbar buttons */
        QScrollBar:horizontal, QScrollBar:vertical {
            border: none;
            background-color: #1F2937;
        }
        
        QScrollBar::handle:horizontal, QScrollBar::handle:vertical {
            background-color: #4F46E5;
            border-radius: 5px;
        }
        
        QScrollBar::handle:horizontal:hover, QScrollBar::handle:vertical:hover {
            background-color: #4338CA;
        }
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }
    """