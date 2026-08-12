/**
 * Shared navigation initialization for all pages.
 * Call initSharedNav(activePage) after DOM load.
 * activePage: 'explore' | 'dashboard' | 'profile' | null
 */
async function initSharedNav(activePage) {
    // Update theme icon on load
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const themeIcon = document.getElementById('theme-icon');
    if (themeIcon && currentTheme === 'light') {
        themeIcon.innerHTML = '<circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>';
    }

    const authRes = await checkAuth();
    const desktopNav = document.getElementById('nav-links-desktop');
    const mobileNav = document.getElementById('nav-links');

    function isActive(page) {
        return activePage === page 
            ? 'style="color: var(--primary); font-weight: 600;"' 
            : 'style="color: var(--text-main); font-weight: 500;"';
    }

    if (authRes.success) {
        const userInitial = authRes.data.full_name.charAt(0).toUpperCase();
        const avatarContent = authRes.data.profile_image 
            ? `<img src="${getImageUrl(authRes.data.profile_image)}" alt="Profile" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;">`
            : userInitial;
            
        if (desktopNav) {
            desktopNav.innerHTML = `
                <div style="position: absolute; left: 50%; transform: translateX(-50%); display: flex; gap: 2rem;">
                    <a href="index.html" ${isActive('explore')}>Explore</a>
                    <a href="dashboard.html" ${isActive('dashboard')}>Post</a>
                    <a href="profile.html" ${isActive('profile')}>Profile</a>
                </div>
                <div style="display: flex; align-items: center; gap: 1rem; margin-left: 1rem;">
                    <a href="profile.html" style="display: flex; align-items: center; gap: 0.5rem; text-decoration: none; color: var(--text-main);">
                        <div style="width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, var(--primary), var(--accent)); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 0.9rem;" id="nav-avatar">${avatarContent}</div>
                    </a>
                    <a href="#" onclick="logout()" class="btn btn-outline" style="padding: 0.4rem 0.8rem; font-size: 0.85rem;">Logout</a>
                </div>
            `;
        }
        if (mobileNav) {
            mobileNav.innerHTML = `
                <a href="index.html" class="nav-item" ${isActive('explore')}>
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                    <span>Explore</span>
                </a>
                <a href="dashboard.html" class="nav-item" ${isActive('dashboard')}>
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>
                    <span>Post</span>
                </a>
                <a href="profile.html" class="nav-item" ${isActive('profile')}>
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                    <span>Profile</span>
                </a>
            `;
        }
    } else {
        if (desktopNav) {
            desktopNav.innerHTML = `
                <div style="position: absolute; left: 50%; transform: translateX(-50%); display: flex; gap: 2rem;">
                    <a href="index.html" ${isActive('explore')}>Explore</a>
                </div>
                <div style="display: flex; align-items: center; gap: 1rem; margin-left: 1rem;">
                    <a href="login.html">Login</a>
                    <a href="register.html" class="btn btn-primary">Sign Up</a>
                </div>
            `;
        }
        if (mobileNav) {
            mobileNav.innerHTML = `
                <a href="index.html" class="nav-item" ${isActive('explore')}>
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                    <span>Explore</span>
                </a>
                <a href="welcome.html" class="nav-item" ${isActive('login')}>
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path><polyline points="10 17 15 12 10 7"></polyline><line x1="15" y1="12" x2="3" y2="12"></line></svg>
                    <span>Sign In</span>
                </a>
                <a href="welcome.html" class="nav-item" ${isActive('register')}>
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="8.5" cy="7" r="4"></circle><line x1="20" y1="8" x2="20" y2="14"></line><line x1="23" y1="11" x2="17" y2="11"></line></svg>
                    <span>Sign Up</span>
                </a>
            `;
        }
    }

    return authRes;
}
