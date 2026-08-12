document.addEventListener('DOMContentLoaded', async () => {
    const authRes = await initSharedNav('explore');
    
    if (authRes && authRes.success) {
        const netCard = document.getElementById('network-card');
        if (netCard) {
            netCard.innerHTML = `
                <h3>Welcome back, ${authRes.data.full_name.split(' ')[0]}!</h3>
                <p style="color: var(--text-muted); font-size: 0.9rem; margin-top: 1rem;">Ready to showcase your latest work?</p>
                <a href="edit_project.html" class="btn btn-primary" style="margin-top: 1rem; width: 100%; text-align: center;">+ Create Post</a>
                <a href="dashboard.html" class="btn btn-outline" style="margin-top: 0.5rem; width: 100%; text-align: center;">View My Posts</a>
            `;
        }
    }
    
    loadProjects();
});

async function initNav() {
    const mobileNav = document.getElementById('nav-links');
    const desktopNav = document.getElementById('nav-links-desktop');
    const authRes = await checkAuth();

    // Update theme icon on load
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const themeIcon = document.getElementById('theme-icon');
    if (themeIcon && currentTheme === 'light') {
        themeIcon.innerHTML = '<circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>';
    }

    const mobileLoggedIn = `
        <a href="index.html" class="nav-item">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            <span>Explore</span>
        </a>
        <a href="dashboard.html" class="nav-item">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
            <span>Dashboard</span>
        </a>
        <a href="profile.html" class="nav-item">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
            <span>Profile</span>
        </a>
        <a href="#" onclick="logout()" class="nav-item">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
            <span>Logout</span>
        </a>
    `;

    const mobileLoggedOut = `
        <a href="index.html" class="nav-item">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            <span>Explore</span>
        </a>
        <a href="login.html" class="nav-item">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path><polyline points="10 17 15 12 10 7"></polyline><line x1="15" y1="12" x2="3" y2="12"></line></svg>
            <span>Login</span>
        </a>
        <a href="register.html" class="nav-item">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="8.5" cy="7" r="4"></circle><line x1="20" y1="8" x2="20" y2="14"></line><line x1="23" y1="11" x2="17" y2="11"></line></svg>
            <span>Sign Up</span>
        </a>
    `;

    if (mobileNav) {
        mobileNav.innerHTML = authRes.success ? mobileLoggedIn : mobileLoggedOut;
    }

    if (desktopNav && authRes.success) {
        desktopNav.innerHTML += `
            <a href="dashboard.html">Dashboard</a>
            <a href="profile.html">Profile</a>
            <a href="#" onclick="logout()" class="btn btn-outline" style="padding: 0.4rem 0.8rem; font-size: 0.85rem;">Logout</a>
        `;
    } else if (desktopNav) {
        desktopNav.innerHTML += `
            <a href="login.html">Login</a>
            <a href="register.html" class="btn btn-primary">Sign Up</a>
        `;
    }
}


async function loadProjects() {
    const grid = document.getElementById('project-grid');
    const loader = document.getElementById('loader');
    const errorBox = document.getElementById('error-box');
    const searchInput = document.getElementById('searchInput').value;
    
    grid.innerHTML = '';
    errorBox.style.display = 'none';
    loader.style.display = 'block';
    
    let endpoint = '/projects';
    if (searchInput.trim() !== '') {
        endpoint += `?search=${encodeURIComponent(searchInput)}`;
    }
    
    const res = await fetchAPI(endpoint);
    loader.style.display = 'none';
    
    if (!res.success) {
        errorBox.textContent = `Error loading projects: ${res.error}`;
        errorBox.style.display = 'block';
        return;
    }
    
    const projects = res.data;
    
    if (projects.length === 0) {
        grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 3rem;">
            <h3>No projects found.</h3>
            <p>Try adjusting your search terms.</p>
        </div>`;
        return;
    }
    
    projects.forEach(p => {
        const statusClass = p.status.includes('Completed') ? 'status-Completed' : 'status-In';
        
        const card = document.createElement('div');
        card.className = 'card';
        
        let imageSection = '';
        if (p.image_url) {
            const urls = p.image_url.split(',').filter(u => u.trim() !== '');
            if (urls.length === 1) {
                imageSection = `<img src="${getImageUrl(urls[0])}" alt="Project Image" class="smart-image-single">`;
            } else if (urls.length > 1) {
                let gridClass = 'grid-more';
                if (urls.length === 2) gridClass = 'grid-2';
                else if (urls.length === 3) gridClass = 'grid-3';
                else if (urls.length === 4) gridClass = 'grid-4';
                
                const displayUrls = urls.slice(0, 4);
                let imagesHtml = '';
                displayUrls.forEach((url, idx) => {
                    if (idx === 3 && urls.length > 4) {
                        imagesHtml += `<div class="more-images-overlay" data-count="${urls.length - 4}"><img src="${getImageUrl(url)}" alt="Project Image"></div>`;
                    } else {
                        imagesHtml += `<img src="${getImageUrl(url)}" alt="Project Image">`;
                    }
                });
                
                imageSection = `
                <div class="smart-image-grid ${gridClass}">
                    ${imagesHtml}
                </div>`;
            }
        }
        
        const isLiked = p.has_liked ? 'liked' : '';
        const heartFill = p.has_liked ? 'var(--danger)' : 'none';
        const heartColor = p.has_liked ? 'var(--danger)' : 'currentColor';
        
        const authorAvatarContent = p.author_image 
            ? `<img src="${getImageUrl(p.author_image)}" alt="Author" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;">`
            : p.author.charAt(0);

        card.innerHTML = `
            <a href="project.html?id=${p.id}" style="text-decoration: none; color: inherit; display: block;">
                <div class="card-header">
                    <div class="author-avatar">${authorAvatarContent}</div>
                    <div class="author-info">
                        <span class="author-name">${p.author}</span>
                        <span class="author-meta">${p.category} • ${p.status}</span>
                    </div>
                </div>
                
                <h3 class="card-title">${p.title}</h3>
                <p class="card-desc">${p.description.substring(0, 200)}${p.description.length > 200 ? '... see more' : ''}</p>
                
                ${imageSection}
            </a>
            
            <div class="interaction-bar">
                <button class="interaction-btn like-btn ${isLiked}" data-id="${p.id}">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="${heartFill}" stroke="${heartColor}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                    </svg>
                    <span class="like-count">${p.like_count || 0}</span>
                </button>
                <button class="interaction-btn comment-btn" data-id="${p.id}">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
                    </svg>
                    <span class="comment-count">${p.comment_count || 0}</span>
                </button>
            </div>
        `;
        grid.appendChild(card);
    });
}

// Event delegation for likes and comments
document.addEventListener('click', async (e) => {
    // Like Button
    const likeBtn = e.target.closest('.like-btn');
    if (likeBtn) {
        e.preventDefault();
        e.stopPropagation();
        const projectId = likeBtn.dataset.id;
        
        // Optimistic UI update
        const isLiked = likeBtn.classList.contains('liked');
        const countSpan = likeBtn.querySelector('.like-count');
        let count = parseInt(countSpan.textContent) || 0;
        
        if (isLiked) {
            likeBtn.classList.remove('liked');
            likeBtn.querySelector('svg').setAttribute('fill', 'none');
            likeBtn.querySelector('svg').setAttribute('stroke', 'currentColor');
            count = Math.max(0, count - 1);
        } else {
            likeBtn.classList.add('liked');
            likeBtn.querySelector('svg').setAttribute('fill', 'var(--danger)');
            likeBtn.querySelector('svg').setAttribute('stroke', 'var(--danger)');
            count += 1;
        }
        countSpan.textContent = count;
        
        // API Call
        const res = await toggleLike(projectId);
        if (!res.success) {
            if (res.error === "Login required") {
                window.location.href = 'login.html';
            }
            // Revert on failure could be implemented here
        } else {
            // Update with actual count from server just to be sure
            countSpan.textContent = res.data.like_count;
        }
    }
    
    // Comment Button
    const commentBtn = e.target.closest('.comment-btn');
    if (commentBtn) {
        e.preventDefault();
        e.stopPropagation();
        const projectId = commentBtn.dataset.id;
        openCommentModal(projectId);
    }
});

let currentCommentProjectId = null;

async function openCommentModal(projectId) {
    let modal = document.getElementById('comment-modal-container');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'comment-modal-container';
        modal.className = 'modal-overlay';
        modal.innerHTML = `
            <div class="comment-modal" onclick="event.stopPropagation()">
                <div class="comment-modal-header">
                    <h3>Comments</h3>
                    <button class="close-modal-btn" onclick="closeCommentModal()">&times;</button>
                </div>
                <div class="comment-list" id="modal-comment-list">
                    <div style="text-align: center; color: var(--text-muted);"><div class="loader" style="width:24px;height:24px;border-width:2px;"></div></div>
                </div>
                <div class="comment-input-area">
                    <input type="text" id="modal-comment-input" placeholder="Add a comment..." onkeypress="if(event.key === 'Enter') submitComment()">
                    <button onclick="submitComment()">Post</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        
        // Close modal when clicking outside
        modal.addEventListener('click', closeCommentModal);
    }
    
    currentCommentProjectId = projectId;
    modal.classList.add('active');
    
    const list = document.getElementById('modal-comment-list');
    list.innerHTML = `<div style="text-align: center; color: var(--text-muted);"><div class="loader" style="width:24px;height:24px;border-width:2px;"></div></div>`;
    
    const res = await getComments(projectId);
    
    if (res.success) {
        renderComments(res.data);
    } else {
        list.innerHTML = `<p style="color: var(--danger); text-align:center;">Failed to load comments.</p>`;
    }
}

function closeCommentModal() {
    const modal = document.getElementById('comment-modal-container');
    if (modal) {
        modal.classList.remove('active');
    }
}

async function renderComments(comments) {
    const list = document.getElementById('modal-comment-list');
    list.innerHTML = '';
    
    if (comments.length === 0) {
        list.innerHTML = `<p style="text-align:center; color: var(--text-muted); margin-top:2rem;">No comments yet. Be the first!</p>`;
        return;
    }
    
    const authRes = await checkAuth();
    const currentUserId = authRes.success ? authRes.data.id : null;
    
    comments.forEach(c => {
        const date = new Date(c.created_at).toLocaleDateString();
        const canDelete = currentUserId === c.user_id;
        
        const avatarContent = c.profile_image
            ? `<img src="${getImageUrl(c.profile_image)}" alt="User" style="width:100%; height:100%; object-fit:cover; border-radius:50%;">`
            : c.full_name.charAt(0);
            
        const item = document.createElement('div');
        item.className = 'comment-item';
        item.innerHTML = `
            <div class="comment-avatar">${avatarContent}</div>
            <div class="comment-content">
                <div class="comment-author">
                    <span>${c.full_name}</span>
                    <span class="comment-date">${date}</span>
                </div>
                <div class="comment-text">${c.content.replace(/</g, "&lt;").replace(/>/g, "&gt;")}</div>
                ${canDelete ? `<button class="delete-comment-btn" onclick="deleteCommentUI(${c.id}, this)">Delete</button>` : ''}
            </div>
        `;
        list.appendChild(item);
    });
}

async function submitComment() {
    if (!currentCommentProjectId) return;
    const input = document.getElementById('modal-comment-input');
    const content = input.value.trim();
    if (!content) return;
    
    input.disabled = true;
    const res = await postComment(currentCommentProjectId, content);
    input.disabled = false;
    
    if (res.success) {
        input.value = '';
        // Reload comments
        const commentsRes = await getComments(currentCommentProjectId);
        if (commentsRes.success) {
            renderComments(commentsRes.data);
            
            // Update counter on the button
            const btn = document.querySelector(`.comment-btn[data-id="${currentCommentProjectId}"] .comment-count`);
            if (btn) btn.textContent = commentsRes.data.length;
        }
    } else {
        if (res.error === "Login required") {
            window.location.href = 'login.html';
        } else {
            alert(res.error || "Failed to post comment");
        }
    }
}

async function deleteCommentUI(commentId, btnElement) {
    if (!confirm("Are you sure you want to delete this comment?")) return;
    
    const res = await deleteComment(commentId);
    if (res.success) {
        // Remove from DOM
        btnElement.closest('.comment-item').remove();
        
        // Update counter on the button
        const btn = document.querySelector(`.comment-btn[data-id="${currentCommentProjectId}"] .comment-count`);
        if (btn) {
            const currentCount = parseInt(btn.textContent) || 1;
            btn.textContent = currentCount - 1;
        }
        
        // If empty
        const list = document.getElementById('modal-comment-list');
        if (list.children.length === 0) {
            list.innerHTML = `<p style="text-align:center; color: var(--text-muted); margin-top:2rem;">No comments yet. Be the first!</p>`;
        }
    } else {
        alert(res.error || "Failed to delete comment");
    }
}
