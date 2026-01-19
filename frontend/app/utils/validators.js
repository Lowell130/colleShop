
export const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
};

export const validatePhone = (phone) => {
    // Allows optional +39, spaces, dashes. Min 6 digits, Max 15.
    const re = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/im;
    // Simpler permissive check: mostly digits, length 6-15
    const clean = phone.replace(/[\s\-\+\(\)]/g, '');
    return clean.length >= 6 && clean.length <= 15 && /^\d+$/.test(clean);
};

export const validateTaxCode = (cf) => {
    if (!cf) return false;
    // Basic format check for Italian CF: 16 alphanumeric characters
    // A stricter regex: 6 letters, 2 digits, 1 letter, 2 digits, 1 letter, 3 digits, 1 letter
    const re = /^[A-Z]{6}[0-9LMNPQRSTUV]{2}[A-Z][0-9LMNPQRSTUV]{2}[A-Z][0-9LMNPQRSTUV]{3}[A-Z]$/i;
    return re.test(cf);
};

export const validateZipCode = (zip) => {
    // Italian CAP is 5 digits
    const re = /^\d{5}$/;
    return re.test(zip);
};
