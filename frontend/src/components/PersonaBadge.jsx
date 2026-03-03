import React from 'react';

const PersonaBadge = ({ persona }) => {
  const getPersonaStyle = (p) => {
    switch (p) {
      case 'technical_expert':
        return { bg: '#e3f2fd', color: '#1976d2', label: 'Technical Expert' };
      case 'frustrated_user':
        return { bg: '#ffebee', color: '#d32f2f', label: 'Frustrated User' };
      case 'business_executive':
        return { bg: '#f3e5f5', color: '#7b1fa2', label: 'Business Executive' };
      default:
        return { bg: '#f5f5f5', color: '#616161', label: 'General User' };
    }
  };

  const style = getPersonaStyle(persona);

  return (
    <span style={{
      backgroundColor: style.bg,
      color: style.color,
      padding: '4px 12px',
      borderRadius: '16px',
      fontSize: '0.75rem',
      fontWeight: '600',
      textTransform: 'uppercase',
      letterSpacing: '0.5px',
      display: 'inline-block',
      marginBottom: '8px'
    }}>
      {style.label}
    </span>
  );
};

export default PersonaBadge;
