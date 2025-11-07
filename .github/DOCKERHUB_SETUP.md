# DockerHub Setup for GitHub Actions

The `docker-image.yml` workflow will **build** the Docker image on every push to `main`, but will only **push** to DockerHub if credentials are configured.

## Option 1: Skip DockerHub (Build Only)

If you don't want to push to DockerHub, you don't need to do anything. The workflow will:
- ✅ Build the Docker image
- ❌ Skip pushing (no error)

## Option 2: Push to DockerHub

If you want to push images to DockerHub, follow these steps:

### 1. Create a DockerHub Account
- Sign up at https://hub.docker.com (if you don't have an account)

### 2. Create an Access Token
1. Go to DockerHub → Account Settings → Security
2. Click "New Access Token"
3. Give it a name (e.g., "github-actions")
4. Set permissions to "Read, Write, Delete"
5. Copy the token (you won't see it again!)

### 3. Add Secrets to GitHub Repository
1. Go to your GitHub repository
2. Navigate to: **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Add two secrets:

   **Secret 1:**
   - Name: `DOCKERHUB_USERNAME`
   - Value: Your DockerHub username

   **Secret 2:**
   - Name: `DOCKERHUB_TOKEN`
   - Value: The access token you created in step 2

### 4. Verify Setup
After adding the secrets, the next push to `main` will:
- ✅ Build the Docker image
- ✅ Push to DockerHub as: `your-username/booking-platform:latest`
- ✅ Also tag with commit SHA: `your-username/booking-platform:<sha>`

## Manual Workflow Trigger

You can also manually trigger the workflow:
1. Go to **Actions** tab in your repository
2. Select **"Build and push Docker image"**
3. Click **"Run workflow"**

